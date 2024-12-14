# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=bad-indentation

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
    try:
        # get information from the request body
        body_data = request.get_json()

        # create stock instance
        new_stock = Stock(
            stock_name=body_data.get("stock_name"),
            ticker=body_data.get("ticker"),
            stock_price=body_data.get("stock_price"),
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

# Read all - /stocks - GET
@stocks_bp.route("/")
def get_stocks():
    stmt = db.select(Stock)
    stocks_list = db.session.scalars(stmt)
    data = stocks_schema.dump(stocks_list)
    return data

# Read one - /stocks/id - GET
@stocks_bp.route("/<int:stock_id>")
def get_stock(stock_id):
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
        # find stock with id to update
        stmt = db.select(Stock).filter_by(id=stock_id)
        stock = db.session.scalar(stmt)
        # get the data to be updated from the request body
        body_data = request.get_json()
        # if stock exists
        if stock:
            # update the stock data field
            stock.stock_name=body_data.get("stock_name") or stock.stock_name
            stock.ticker=body_data.get("ticker") or stock.ticker
            stock.stock_price=body_data.get("stock_price") or stock.stock_price
            # commit changes
            db.session.commit()
            # return updated data
            return stock_schema.dump(stock), 200
        else:
            # if stock doesn't exist
            return {"message": f"Stock with id {stock_id} does not exist"}, 404

# Delete - /stocks/id - DELETE
@stocks_bp.route("/<int:stock_id>", methods=["DELETE"])
def delete_stock(stock_id):
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
    