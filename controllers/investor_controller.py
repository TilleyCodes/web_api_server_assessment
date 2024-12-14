# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

from datetime import date

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models import Investor
from schemas.investor_schema import investors_schema, investor_schema

investors_bp = Blueprint("investors", __name__, url_prefix="/investors")

# Create - /investors - POST
@investors_bp.route("/", methods=["POST"])
def create_investor():
    try:
        # get information from the request body
        body_data = request.get_json()

        # parse reg_date
        registration_date = (
            date.fromisoformat(body_data.get("registration_date"))
            if body_data.get("registration_date")
            else None
        )

        # create investor instance
        new_investor = Investor(
            f_name=body_data.get("f_name"),
            l_name=body_data.get("l_name"),
            email=body_data.get("email"),
            registration_date=registration_date,
            account_balance=body_data.get("account_balance")
        )
        # add to the session
        db.session.add(new_investor)
        # commit
        db.session.commit()
        # return a response
        return investor_schema.dump(new_investor), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not null violation
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409

        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # unique constraint violation
            return {"message": "Email address already in use"}, 409
    except ValueError: # invalide date format
        return {"message": "Invalid date format. Please use YYYY-MM-DD"}, 400

# Read all - /investors - GET
@investors_bp.route("/")
def get_investors():
    stmt = db.select(Investor)
    investors_list = db.session.scalars(stmt)
    data = investors_schema.dump(investors_list)
    return data

# Read one - /investors/id - GET
@investors_bp.route("/<int:investor_id>")
def get_investor(investor_id):
    stmt = db.select(Investor).filter_by(id=investor_id)
    investor = db.session.scalar(stmt)
    if investor:
        data = investor_schema.dump(investor)
        return data
    else:
        return {"message": f"Investor with id {investor_id} does not exist"}, 404

# Update - /investors/id - PUT or PATCH
@investors_bp.route("/<int:investor_id>", methods=["PUT", "PATCH"])
def update_investor(investor_id):
    try:
        # find investor with id to update
        stmt = db.select(Investor).filter_by(id=investor_id)
        investor = db.session.scalar(stmt)
        # get the data to be updated from the request body
        body_data = request.get_json()
        # if investor exists
        if investor:
            # update the investor data field
            investor.f_name=body_data.get("f_name") or investor.f_name
            investor.l_name=body_data.get("l_name") or investor.l_name
            investor.email=body_data.get("email") or investor.email
            investor.registration_date=(
                date.fromisoformat(body_data["registration_date"])
                if "registration_date" in body_data
                else investor.registration_date
            )
            investor.account_balance=body_data.get("account_balance") or investor.account_balance
            # commit changes
            db.session.commit()
            # return updated data
            return investor_schema.dump(investor), 200
        else:
            # if investor doesn't exist
            return {"message": f"Investor with id {investor_id} does not exist"}, 404
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # unique constraint violation
            return {"message": "Email address already in use"}, 409
    except ValueError: # invalide date format
        return {"message": "Invalid date format. Please use YYYY-MM-DD"}, 400

# Delete - /investors/id - DELETE
@investors_bp.route("/<int:investor_id>", methods=["DELETE"])
def delete_investor(investor_id):
    # find the investor to delete using id
    stmt = db.select(Investor).filter_by(id=investor_id)
    investor = db.session.scalar(stmt)
    if investor:
        # delete
        db.session.delete(investor)
        db.session.commit()
        # return response
        return {"message": f"Investor '{investor.f_name}' deleted successfully"}
    else:
        # return error response
        return {"message": f"Investor with id {investor_id} does not exist"}, 404
    