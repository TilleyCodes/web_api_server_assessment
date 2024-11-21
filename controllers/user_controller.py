from datetime import date

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.user import User 
from schemas.user_schema import users_schema, user_schema

users_bp = Blueprint("users", __name__, url_prefix="/users")

# Create - /users - POST
@users_bp.route("/", methods=["POST"])
def create_user():
    try:
        # get information from the request body
        body_data = request.get_json()

        # parse acc_open_date
        account_open_date = (
            date.fromisoformat(body_data.get("account_open_date"))
            if body_data.get("account_open_date")
            else None
        )

        # create user instance
        new_user = User(
            f_name=body_data.get("f_name"),
            l_name=body_data.get("l_name"),
            email=body_data.get("email"),
            account_open_date=account_open_date,
            account_balance=body_data.get("account_balance")
        )
        # add to the session
        db.session.add(new_user)
        # commit
        db.session.commit()
        # return a response
        return user_schema.dump(new_user), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not null violation
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # unique constraint violation
            return {"message": "Email address already in use"}, 409
    except ValueError: # invalide date format
        return {"message": "Invalid date format. Use YYYY-MM-DD"}, 400
        
# Read all - /users - GET
@users_bp.route("/")
def get_users():
    stmt = db.select(User)
    users_list = db.session.scalars(stmt)
    data = users_schema.dump(users_list)
    return data

# Read one - /users/id - GET
@users_bp.route("/<int:user_id>")
def get_user(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        data = user_schema.dump(user)
        return data
    else:
        return {"message": f"User with id {user_id} does not exist"}, 404
    

# Update - /users/id - PUT or PATCH
@users_bp.route("/<int:user_id>", methods=["PUT", "PATCH"])
def update_user(user_id):
    try:
        # find user with id to update
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        # get the data to be updated from the request body
        body_data = request.get_json()
        # if user exists
        if user:
            # update the user data fields
            user.f_name=body_data.get("f_name") or user.f_name
            user.l_name=body_data.get("l_name") or user.l_name
            user.email=body_data.get("email") or user.email
            user.account_open_date=(
                date.fromisoformat(body_data["account_open_date"])
                if "account_open_date" in body_data
                else user.account_open_date
            )
            user.account_balance=body_data.get("account_balance") or user.account_balance
            # commit changes
            db.session.commit()
            # return updated data
            return user_schema.dump(user), 200
        else:
            # if user doesn't exist
            return {"message": f"User with id {user_id} does not exist"}, 404
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # unique constraint violation
            return {"message": "Email address already in use"}, 409
        return {"message": "Email address already in use"}, 409
    except ValueError: # invalide date format
        return {"message": "Invalid date format. Use YYYY-MM-DD"}, 400
    
# Delete - /users/id - DELETE 