from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.watchlist import Watchlist
from models.user import User
from models.stock import Stock
from schemas.watchlist_schema import watchlists_schema, watchlist_schema

watchlists_bp = Blueprint("watchlists", __name__, url_prefix="/watchlists")

# Create - /watchlists - POST
@watchlists_bp.route("/", methods=["POST"])
def create_watchlist():
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
        
        # create watchlist instance
        new_watchlist = Watchlist(
            user_id=user_id,
            stock_id=user_id
        )
        # add to the session
        db.session.add(new_watchlist)
        # commit
        db.session.commit()
        # return a response
        return watchlist_schema.dump(new_watchlist), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not null violation
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 400
        
# Read all - /watchlists - GET
@watchlists_bp.route("/", methods=["GET"])
def get_watchlists():
    stmt = db.select(Watchlist)
    watchlists_list = db.session.scalars(stmt)
    data = watchlists_schema.dump(watchlists_list)
    return data, 200

# Read one - /watchlists/id - GET
@watchlists_bp.route("/<int:watchlist_id>")
def get_watchlist(watchlist_id):
    stmt = db.select(Watchlist).filter_by(id=watchlist_id)
    watchlist = db.session.scalar(stmt)
    if watchlist:
        data = watchlist_schema.dump(watchlist)
        return data, 200
    else:
        return {"message": f"Watchlist with id {watchlist_id} does not exist"}, 404
    
# Update - /watchlists/id - PUT or PATCH
@watchlists_bp.route("/<int:watchlist_id>", methods=["PUT", "PATCH"])
def update_watchlist(watchlist_id):
    try:
        # find watchlist with id to update
        stmt = db.select(Watchlist).filter_by(id=watchlist_id)
        watchlist = db.session.scalar(stmt)
        # if watchlist id does not exist
        if not watchlist:
            return {"message": f"Watchlist with id {watchlist_id} does not exist"}, 404
        
        # get the data to be updated from the request body with error handling
        body_data = request.get_json()
        if not body_data:
            return {"message": "Request body is missing or invalid"}, 400
                   
              # Validate user_id if provided
        if "user_id" in body_data:
            user = db.session.get(User, body_data["user_id"])
            if not user:
                return {"message": f"Invalid user_id: {body_data['user_id']}. User does not exist."}, 404
            watchlist.user_id = body_data["user_id"]

        # Validate stock_id if provided
        if "stock_id" in body_data:
            stock = db.session.get(Stock, body_data["stock_id"])
            if not stock:
                return {"message": f"Invalid stock_id: {body_data['stock_id']}. Stock does not exist."}, 404
            watchlist.stock_id = body_data["stock_id"]   

            # commit changes
            db.session.commit()
            # return updated data
            return watchlist_schema.dump(watchlist), 200
        else:
            # if watchlist doesn't exist
            return {"message": f"Watchlist with id {watchlist_id} does not exist"}, 404
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not null violation
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        
# Delete - /watchlists/id - DELETE 
@watchlists_bp.route("/<int:watchlist_id>", methods=["DELETE"])
def delete_watchlist(watchlist_id):
    # find the watchlist to delete using id
    stmt = db.select(Watchlist).filter_by(id=watchlist_id)
    watchlist = db.session.scalar(stmt)
    if watchlist:
        # delete
        db.session.delete(watchlist)
        db.session.commit()
        # return response
        return {"message": f"Watchlist with id'{watchlist.id}' deleted successfully"}, 200
    else:
        # return error response
        return {"message": f"Watchlist with id {watchlist_id} does not exist"}, 404