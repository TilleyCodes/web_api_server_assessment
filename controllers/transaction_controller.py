from datetime import date

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.order import Order
from models.user import User
from models.transaction import Transaction
from enums import TransactionType
from schemas.transaction_schema import transactions_schema, transaction_schema

transactions_bp = Blueprint("transactions", __name__, url_prefix="/transactions")

# Create - /transactions - POST
@transactions_bp.route("/", methods=["POST"])
def create_transaction():
    try:
        # get data from the request body with error handling
        body_data = request.get_json()
        if not body_data:
            return {"messgae": "Request body is missing or invalid"}, 400

        # validate & parse trade_date
        transaction_date = (
            date.fromisoformat(body_data.get("transaction_date"))
            if body_data.get("transaction_date")
            else None
        )
        # validate and convert transaction_type enum
        try:
            transaction_type = TransactionType(body_data.get("transaction_type"))
        except ValueError:
            return{"message": f"Invalid transaction type. Please use one of the following: {[e.value for e in TransactionType]}"}, 400
        
        # Check for valid user_id
        user_id = body_data.get("user_id")
        user = db.session.get(User, user_id)  # Check if user exists
        if not user:
            return {"message": f"Invalid user_id: {user_id}. User does not exist."}, 404

        # Check for valid order_id
        order_id = body_data.get("order_id")
        order = db.session.get(Order, order_id)  # Check if order exists
        if not order:
            return {"message": f"Invalid order_id: {order_id} does not exist."}, 404
        
        # create transaction instance
        new_transaction = Transaction(
            transaction_date=transaction_date,
            transaction_type=transaction_type,
            amount=body_data.get("amount"),
            user_id=user_id,
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
    
    except ValueError: # invalide date format
        return {"message": "Invalid date format. Please use YYYY-MM-DD"}, 400
        
# Read all - /transactions - GET
@transactions_bp.route("/", methods=["GET"])
def get_transactions():
    stmt = db.select(Transaction)
    transactions_list = db.session.scalars(stmt)
    data = transactions_schema.dump(transactions_list)
    return data, 200

# Read one - /transactions/id - GET
@transactions_bp.route("/<int:transaction_id>")
def get_transaction(transaction_id):
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
            return {"message": "Request body is missing or invalid"}, 400
        
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
    
              # Validate user_id if provided
        if "user_id" in body_data:
            user = db.session.get(User, body_data["user_id"])
            if not user:
                return {"message": f"Invalid user_id: {body_data['user_id']}. User does not exist."}, 404
            transaction.user_id = body_data["user_id"]

        # Validate order_id if provided
        if "order_id" in body_data:
            order = db.session.get(Order, body_data["order_id"])
            if not order:
                return {"message": f"Invalid order_id: {body_data['stock_id']} does not exist."}, 404
            transaction.order_id = body_data["order_id"]
            
            transaction.amount=body_data.get("amount") or transaction.amount    

            # commit changes
            db.session.commit()
            # return updated data
            return transaction_schema.dump(order), 200
        else:
            # if order doesn't exist
            return {"message": f"Transaction with id {transaction_id} does not exist"}, 404
    except ValueError: # invalide date format
        return {"message": "Invalid date format. Please use YYYY-MM-DD"}, 400
    
# Delete - /transactions/id - DELETE 
@transactions_bp.route("/<int:transaction_id>", methods=["DELETE"])
def delete_order(transaction_id):
    # find the transaction to delete using id
    stmt = db.select(Transaction).filter_by(id=transaction_id)
    transaction = db.session.scalar(stmt)
    if transaction:
        # delete
        db.session.delete(transaction)
        db.session.commit()
        # return response
        return {"message": f"Transaction with id'{transaction.id}' deleted successfully"}, 200
    else:
        # return error response
        return {"message": f"Transaction with id {transaction_id} does not exist"}, 404