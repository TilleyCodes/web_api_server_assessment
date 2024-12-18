# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring


from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models import Portfolio, Investor, Stock
from schemas.portfolio_schema import portfolios_schema, portfolio_schema

portfolios_bp = Blueprint("portfolios", __name__, url_prefix="/portfolios")

# Create - /portfolios - POST
@portfolios_bp.route("/", methods=["POST"])
def create_portfolio():
    try:
        # get data from the request body with error handling
        body_data = request.get_json()
        if not body_data:
            return {"messgae": "Request body is missing or invalid"}, 400

        # Check for valid investor_id
        investor_id = body_data.get("investor_id")
        investor = db.session.get(Investor, investor_id)  # Check if investor exists
        if not investor:
            return {"message": f"Invalid investor_id: {investor_id}. Investor does not exist."}, 404

        # Check for valid stock_id
        stock_id = body_data.get("stock_id")
        stock = db.session.get(Stock, stock_id)  # Check if stock exists
        if not stock:
            return {"message": f"Invalid stock_id: {stock_id}. Stock does not exist."}, 404

        # Check for numeric and non zero value
        number_of_units = body_data.get("number_of_units")
        if not isinstance(number_of_units, int) or number_of_units <= 0:
            return {"message": "Number of units must be a numeric value and greater than 0."}, 400

        # create portfolio instance
        new_portfolio = Portfolio(
            number_of_units=number_of_units,
            investor_id=investor_id,
            stock_id=stock_id
        )
        # add to the session
        db.session.add(new_portfolio)
        # commit
        db.session.commit()
        # return a response
        return portfolio_schema.dump(new_portfolio), 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not null violation
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 400
        return {"message": "An unexpected error occurred."}, 500

# Read all - /portfolios - GET
@portfolios_bp.route("/", methods=["GET"])
def get_portfolios():
    stmt = db.select(Portfolio)

    investor_id = request.args.get("investor_id")
    if investor_id:
        try:
            investor_id =int(investor_id) #validating investor id is a number and catching error
            stmt =stmt.filter(Portfolio.investor_id==investor_id)
        except ValueError:
            return {"message": "Investor ID must be a number."}, 400

    stock_id = request.args.get("stock_id")
    if stock_id:
        try:
            stock_id = int(stock_id) #validating istock id is a number and catching error
            stmt =stmt.filter(Portfolio.stock_id==stock_id)
        except ValueError:
            return {"message": "Stock ID must be a number."}, 400
    portfolios_list = db.session.scalars(stmt).all()
    if not portfolios_list:
        return {"message": "No orders found with provided filters."}, 404
    data = portfolios_schema.dump(portfolios_list)
    return data, 200

# Read one - /portfolios/id - GET
@portfolios_bp.route("/<int:portfolio_id>")
def get_portfolio(portfolio_id):
    stmt = db.select(Portfolio).filter_by(id=portfolio_id)
    portfolio = db.session.scalar(stmt)
    if portfolio:
        data = portfolio_schema.dump(portfolio)
        return data, 200
    else:
        return {"message": f"Portfolio with id {portfolio_id} does not exist"}, 404

# Update - /portfolios/id - PUT or PATCH
@portfolios_bp.route("/<int:portfolio_id>", methods=["PUT", "PATCH"])
def update_portfolio(portfolio_id):
    try:
        # find portfolio with id to update
        stmt = db.select(Portfolio).filter_by(id=portfolio_id)
        portfolio = db.session.scalar(stmt)
        # if portfolio id does not exist
        if not portfolio:
            return {"message": f"Portfolio with id {portfolio_id} does not exist"}, 404

        # get the data to be updated from the request body with error handling
        body_data = request.get_json()
        if not body_data:
            return {"message": "Request body is missing or invalid"}, 400

              # Validate investor_id if provided
        if "investor_id" in body_data:
            investor = db.session.get(Investor, body_data["investor_id"])
            if not investor:
                return {"message": f"Invalid investor_id: {body_data['investor_id']}. Investor does not exist."}, 404
            portfolio.investor_id = body_data["investor_id"]

        # Validate stock_id if provided
        if "stock_id" in body_data:
            stock = db.session.get(Stock, body_data["stock_id"])
            if not stock:
                return {"message": f"Invalid stock_id: {body_data['stock_id']}. Stock does not exist."}, 404
            portfolio.stock_id = body_data["stock_id"]

        # Validate number_of_units non zero and numeric value
        if "number_of_units" in body_data:
            number_of_units = body_data["number_of_units"]
            if not isinstance(number_of_units, int) or number_of_units <= 0:
                return {"message": "Number of units must be a numeric value and greater than 0."}, 400
            portfolio.number_of_units = number_of_units

            # commit changes
            db.session.commit()
            # return updated data
            return portfolio_schema.dump(portfolio), 200

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not null violation
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        return {"message": "An unexpected error occurred."}, 500

# Delete - /portfolios/id - DELETE
@portfolios_bp.route("/<int:portfolio_id>", methods=["DELETE"])
def delete_portfolio(portfolio_id):
    # find the portfolio to delete using id
    stmt = db.select(Portfolio).filter_by(id=portfolio_id)
    portfolio = db.session.scalar(stmt)
    if portfolio:
        # delete
        db.session.delete(portfolio)
        db.session.commit()
        # return response
        return {"message": f"Portfolio with id' {portfolio.id}' deleted successfully"}, 200
    else:
        # return error response
        return {"message": f"Portfolio with id {portfolio_id} does not exist"}, 404
    