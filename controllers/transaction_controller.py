# pylint: disable=line-too-long

"""
Blueprint for Transaction CRUD operations.
"""

from datetime import date

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models import Investor, Order, Transaction
from enums import TransactionType
from schemas.transaction_schema import transactions_schema, transaction_schema

transactions_bp = Blueprint("transactions", __name__, url_prefix="/transactions")

# Create - /transactions - POST
@transactions_bp.route("/", methods=["POST"])
def create_transaction():
    """
    Function to create a new transaction.
    """
    try:
        # get data from the request body with error handling
        body_data = request.get_json()
        if not body_data:
            return {"message": "Request body is missing or contains invalid data"}, 400

        # validate & parse transaction_date
        transaction_date = (
            date.fromisoformat(body_data.get("transaction_date"))
            if body_data.get("transaction_date")
            else date.today()
        )
        # validate and convert transaction_type enum
        try:
            transaction_type = TransactionType(body_data.get("transaction_type"))
        except ValueError:
            return{"message": f"Invalid transaction type. Please use one of the following: {[e.value for e in TransactionType]}"}, 400

        # Check for numeric and non zero value
        try:
            amount = float(body_data.get("amount"))
            if amount <= 0:
                return {"message": "Amount must be greater than 0."}, 400
        except (ValueError, TypeError):
            return {"message": "Amount must be a numeric value."}, 400

        # Check for valid investor_id
        investor_id = body_data.get("investor_id")
        investor = db.session.get(Investor, investor_id)  # Check if investor exists
        if not investor:
            return {"message": f"Invalid investor_id: {investor_id}. Investor does not exist."}, 404

        # Check for valid order_id
        order_id = body_data.get("order_id")
        order = db.session.get(Order, order_id)  # Check if order exists
        if not order:
            return {"message": f"Invalid order_id: {order_id} does not exist."}, 404

        # create transaction instance
        new_transaction = Transaction(
            transaction_date=transaction_date,
            transaction_type=transaction_type,
            amount=amount,
            investor_id=investor_id,
            order_id=order_id
        )
        # add to the session
        db.session.add(new_transaction)
        # commit
        db.session.commit()
        # return a response
        return transaction_schema.dump(new_transaction), 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not null violation
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 400

        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # unique constraint violation
            return {"message": "Order ID already associated with a transaction"}, 409

    except ValueError: # invalid date format
        return {"message": "Invalid date format. Please use YYYY-MM-DD"}, 400
    return {"message": "An unexpected error occurred."}, 500

# Read all - /transactions - GET
@transactions_bp.route("/", methods=["GET"])
def get_transactions():
    """
    Function to retrieve all transactions, optionally filtered by query parameters.
    """
    stmt = db.select(Transaction)

    investor_id = request.args.get("investor_id")
    if investor_id:
        try:
            investor_id =int(investor_id) #validating investor id is a number and catching error
            stmt =stmt.filter(Transaction.investor_id==investor_id)
        except ValueError:
            return {"message": "Investor ID must be a number."}, 400

    order_id = request.args.get("order_id")
    if order_id:
        try:
            order_id = int(order_id) #validating order id is a number and catching error
            stmt =stmt.filter(Transaction.order_id==order_id)
        except ValueError:
            return {"message": "Order ID must be a number."}, 400

    transaction_type = request.args.get("transaction_type")
    if transaction_type:
        try:
            valid_transaction_type = TransactionType(transaction_type)  # check enum to validate transaction type
            stmt = stmt.filter(Transaction.transaction_type == valid_transaction_type)
        except ValueError:
            valid_types = [e.value for e in TransactionType]
            return {"message": f"Invalid transaction_type. Valid values are: {valid_types}"}, 400

    stmt =stmt.order_by(Transaction.id)
    transactions_list = db.session.scalars(stmt).all()
    if not transactions_list:
        return {"message": "No transactions found with provided filters."}, 404
    data = transactions_schema.dump(transactions_list)
    return data, 200

# Read one - /transactions/id - GET
@transactions_bp.route("/<int:transaction_id>")
def get_transaction(transaction_id):
    """
    Function to retrieve a transaction by ID.
    """
    stmt = db.select(Transaction).filter_by(id=transaction_id)
    transaction = db.session.scalar(stmt)
    if transaction:
        data = transaction_schema.dump(transaction)
        return data, 200
    else:
        return {"message": f"Transaction with id {transaction_id} does not exist"}, 404

# Update - /transactions/id - PUT or PATCH
@transactions_bp.route("/<int:transaction_id>", methods=["PUT", "PATCH"])
def update_transaction(transaction_id):
    """
    Function to update a transaction by ID.
    """
    try:
        # find transaction with id to update
        stmt = db.select(Transaction).filter_by(id=transaction_id)
        transaction = db.session.scalar(stmt)
        # if transaction id does not exist
        if not transaction:
            return {"message": f"Transaction with id {transaction_id} does not exist"}, 404

        # get the data to be updated from the request body with error handling
        body_data = request.get_json()
        if not body_data:
            return {"message": "Request body is missing or contains invalid data"}, 400

        # if transaction exists
        if transaction:
            # update the transaction data field
            transaction.transaction_date=(
                date.fromisoformat(body_data["transaction_date"])
                if "transaction_date" in body_data
                else transaction.transaction_date
            )
        # validate and update transaction_type enum
        if "transaction_type" in body_data:
            try:
                transaction.transaction_type = TransactionType(body_data["transaction_type"])
            except ValueError:
                return{"message": f"Invalid transaction type. Please use one of the following: {[e.value for e in TransactionType]}"}, 400

        # Validate and update amount
        if "amount" in body_data:
            try:
                amount = float(body_data.get("amount"))
                if amount <= 0:
                    return {"message": "Net amount must be greater than 0."}, 400
            except (ValueError, TypeError):
                return {"message": "Net amount must be a numeric value."}, 400

        # Validate investor_id if provided
        if "investor_id" in body_data:
            investor = db.session.get(Investor, body_data["investor_id"])
            if not investor:
                return {"message": f"Invalid investor_id: {body_data['investor_id']}. Investor does not exist."}, 404
            transaction.investor_id = body_data["investor_id"]

        # Validate order_id if provided
        if "order_id" in body_data:
            order = db.session.get(Order, body_data["order_id"])
            if not order:
                return {"message": f"Invalid order_id: {body_data['order_id']} does not exist."}, 404
            transaction.order_id = body_data["order_id"]

            # commit changes
            db.session.commit()
            # return updated data
            return transaction_schema.dump(order), 200
    except ValueError: # invalide date format
        return {"message": "Invalid date format. Please use YYYY-MM-DD"}, 400
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 400
    return {"message": "An unexpected error occurred."}, 500

# Delete - /transactions/id - DELETE
@transactions_bp.route("/<int:transaction_id>", methods=["DELETE"])
def delete_order(transaction_id):
    """
    Function to delete a transaction by ID.
    """
    # find the transaction to delete using id
    stmt = db.select(Transaction).filter_by(id=transaction_id)
    transaction = db.session.scalar(stmt)
    if transaction:
        # delete
        db.session.delete(transaction)
        db.session.commit()
        # return response
        return {"message": f"Transaction with id '{transaction.id}' deleted successfully"}, 200
    else:
        # return error response
        return {"message": f"Transaction with id {transaction_id} does not exist"}, 404
    