from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.portfolio import Portfolio
from models.user import User
from models.stock import Stock
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
        
        # Check for valid user_id
        user_id = body_data.get("user_id")
        user = db.session.get(User, user_id)  # Check if user exists
        if not user:
            return {"message": f"Invalid user_id: {user_id}. User does not exist."}, 404

        # Check for valid stock_id
        stock_id = body_data.get("stock_id")
        stock = db.session.get(Stock, stock_id)  # Check if stock exists
        if not stock:
            return {"message": f"Invalid stock_id: {stock_id}. Stock does not exist."}, 404
        
        # create portfolio instance
        new_portfolio = Portfolio(
            number_of_units=body_data.get("number_of_units"),
            user_id=user_id,
            stock_id=user_id
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
        
# Read all - /portfolios - GET
@portfolios_bp.route("/", methods=["GET"])
def get_portfolios():
    stmt = db.select(Portfolio)
    portfolios_list = db.session.scalars(stmt)
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
                   
              # Validate user_id if provided
        if "user_id" in body_data:
            user = db.session.get(User, body_data["user_id"])
            if not user:
                return {"message": f"Invalid user_id: {body_data['user_id']}. User does not exist."}, 404
            portfolio.user_id = body_data["user_id"]

        # Validate stock_id if provided
        if "stock_id" in body_data:
            stock = db.session.get(Stock, body_data["stock_id"])
            if not stock:
                return {"message": f"Invalid stock_id: {body_data['stock_id']}. Stock does not exist."}, 404
            portfolio.stock_id = body_data["stock_id"]
            
            portfolio.number_of_units=body_data.get("number_of_units") or portfolio.number_of_units    

            # commit changes
            db.session.commit()
            # return updated data
            return portfolio_schema.dump(portfolio), 200
        else:
            # if portfolio doesn't exist
            return {"message": f"Portfolio with id {portfolio_id} does not exist"}, 404
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not null violation
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        
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
        return {"message": f"Portfolio with id'{portfolio.id}' deleted successfully"}, 200
    else:
        # return error response
        return {"message": f"Portfolio with id {portfolio_id} does not exist"}, 404