# pylint: disable=line-too-long
# pylint: disable=bad-indentation

"""
Blueprint for Stock CRUD operations.
"""

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models import Stock
from schemas.stock_schema import stocks_schema, stock_schema

stocks_bp = Blueprint("stocks", __name__, url_prefix="/stocks")

# Create - /stocks - POST
@stocks_bp.route("/", methods=["POST"])
def create_stock():
    """
    Function to create a new stock.
    """
    try:
        # get information from the request body
        body_data = request.get_json()
        if not body_data:
            return {"message": "Request body is missing or contains invalid data"}, 400

        # Check for numeric and non zero/negative value
        stock_price = body_data.get("stock_price")
        try:
            stock_price = float(stock_price)
            if stock_price < 0:
                return {"message": "Stock price must be a non-negative value."}, 400
        except (ValueError, TypeError):
            return {"message": "Stock price must be a numeric value."}, 400

        # create stock instance
        new_stock = Stock(
            stock_name=body_data.get("stock_name"),
            ticker=body_data.get("ticker"),
            stock_price=stock_price,
        )

        db.session.add(new_stock)
        db.session.commit()
        # return a response
        return stock_schema.dump(new_stock), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not null violation
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # unique constraint violation
            return {"message": f"This stock '{body_data.get('stock_name')}' or ticker '{body_data.get('ticker')}' already exists"}, 409
        return {"message": "An unexpected error occurred."}, 500

# Read all - /stocks - GET
@stocks_bp.route("/")
def get_stocks():
    """
    Function to retrieve all stocks with optional query parameters.
    """
    stmt = db.select(Stock)

    ticker = request.args.get("ticker") #query parameter
    if ticker:
        stmt = stmt.filter(Stock.ticker.ilike(f"%{ticker}%")) # For case insensitive filtering

    price = request.args.get("price") #query parameter
    if price:
        try: #  stock_price must be numeric value
            price = float(price)
            stmt = stmt.filter(Stock.stock_price==price)
        except ValueError:
            return {"message": "Stock price must be a numeric value and greater than 0."}, 400

    stmt =stmt.order_by(Stock.id)
    stocks_list = db.session.scalars(stmt).all()
    if not stocks_list:
        return {"message": "No stocks found with provided filters."}, 404
    data = stocks_schema.dump(stocks_list)
    return data

# Read one - /stocks/id - GET
@stocks_bp.route("/<int:stock_id>")
def get_stock(stock_id):
    """
        Function to retrieve a stock by ID.
        """
    stmt = db.select(Stock).filter_by(id=stock_id)
    stock = db.session.scalar(stmt)
    if stock:
        data = stock_schema.dump(stock)
        return data
    else:
        return {"message": f"Stock with id {stock_id} does not exist"}, 404

# Update - /stocks/id - PUT or PATCH
@stocks_bp.route("/<int:stock_id>", methods=["PUT", "PATCH"])
def update_stock(stock_id):
        """
        Function to update a stock by ID.
        """
        # find stock with id to update
        stmt = db.select(Stock).filter_by(id=stock_id)
        stock = db.session.scalar(stmt)
        if not stock:
            return {"message": f"Stock with id {stock_id} does not exist."}, 404
        # get the data to be updated from the request body
        body_data = request.get_json()
        if not body_data:
            return {"message": "Request body is missing or contains invalid data"}, 400
        # if stock exists
        if "stock_price" in body_data:
            try:
                stock_price = float(body_data["stock_price"])
                if stock_price < 0:
                    return {"message": "Stock price must be a non-negative value."}, 400
                stock.stock_price = stock_price
            except (ValueError, TypeError):
                return {"message": "Stock price must be a numeric value."}, 400

        # update the stock data field
        stock.stock_name=body_data.get("stock_name") or stock.stock_name
        stock.ticker=body_data.get("ticker") or stock.ticker
        # commit changes
        db.session.commit()
        # return updated data
        return stock_schema.dump(stock), 200

# Delete - /stocks/id - DELETE
@stocks_bp.route("/<int:stock_id>", methods=["DELETE"])
def delete_stock(stock_id):
    """
    Function to delete a stock by ID.
    """
    # find the stock to delete using id
    stmt = db.select(Stock).filter_by(id=stock_id)
    stock = db.session.scalar(stmt)
    if stock:
        db.session.delete(stock)
        db.session.commit()
        # return response
        return {"message": f"Stock '{stock.stock_name}' deleted successfully"}
    else:
        # return error response
        return {"message": f"Stock with id {stock_id} does not exist"}, 404
    