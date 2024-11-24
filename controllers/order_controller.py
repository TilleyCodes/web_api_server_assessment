from datetime import date

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.order import Order
from models.user import User
from models.stock import Stock
from enums import OrderType, OrderStatus 
from schemas.order_schema import orders_schema, order_schema

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")

# Create - /orders - POST
@orders_bp.route("/", methods=["POST"])
def create_order():
    try:
        # get data from the request body with error handling
        body_data = request.get_json()
        if not body_data:
            return {"messgae": "Request body is missing or invalid"}, 400

        # validate & parse trade_date
        trade_date = (
            date.fromisoformat(body_data.get("trade_date"))
            if body_data.get("trade_date")
            else None
        )
        # validate and convert order_type enum
        try:
            order_type = OrderType(body_data.get("order_type"))
        except ValueError:
            return{"message": f"Invalid order type. Please use one of the following: {[e.value for e in OrderType]}"}, 400
        
        # validate and convert order_status
        try:
            order_status = OrderStatus(body_data.get("order_status"))
        except ValueError:
            return{"message": f"Invalid order status. Please use one of the following: {[e.value for e in OrderStatus]}"}, 400
        
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
        
        # create order instance
        new_order = Order(
            trade_date=trade_date,
            order_type=order_type,
            quantity=body_data.get("quantity"),
            net_amount=body_data.get("net_amount"),
            order_status=order_status,
            user_id=user_id,
            stock_id=user_id
        )
        # add to the session
        db.session.add(new_order)
        # commit
        db.session.commit()
        # return a response
        return order_schema.dump(new_order), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not null violation
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 400
    
    except ValueError: # invalide date format
        return {"message": "Invalid date format. Please use YYYY-MM-DD"}, 400
        
# Read all - /orders - GET
@orders_bp.route("/", methods=["GET"])
def get_orders():
    stmt = db.select(Order)
    orders_list = db.session.scalars(stmt)
    data = orders_schema.dump(orders_list)
    return data, 200

# Read one - /orders/id - GET
@orders_bp.route("/<int:order_id>")
def get_order(order_id):
    stmt = db.select(Order).filter_by(id=order_id)
    order = db.session.scalar(stmt)
    if order:
        data = order_schema.dump(order)
        return data, 200
    else:
        return {"message": f"Order with id {order_id} does not exist"}, 404
    
# Update - /orders/id - PUT or PATCH
@orders_bp.route("/<int:order_id>", methods=["PUT", "PATCH"])
def update_order(order_id):
    try:
        # find order with id to update
        stmt = db.select(Order).filter_by(id=order_id)
        order = db.session.scalar(stmt)
        # if order id does not exist
        if not order:
            return {"message": f"Order with id {order_id} does not exist"}, 404
        
        # get the data to be updated from the request body with error handling
        body_data = request.get_json()
        if not body_data:
            return {"message": "Request body is missing or invalid"}, 400
        
        # if order exists
        if order:
            # update the order data field
            order.trade_date=(
                date.fromisoformat(body_data["trade_date"])
                if "trade_date" in body_data
                else order.trade_date
            )
            # validate and update order_type enum
        if "order_type" in body_data:
            try:
                order.order_type = OrderType(body_data["order_type"])
            except ValueError:
                return{"message": f"Invalid order type. Please use one of the following: {[e.value for e in OrderType]}"}, 400
            
            # validate and update order_status
        if "order_status" in body_data:
            try:
                order.order_status = OrderStatus(body_data["order_status"])
            except ValueError:
                return{"message": f"Invalid order status. Please use one of the following: {[e.value for e in OrderStatus]}"}, 400
              # Validate user_id if provided
        if "user_id" in body_data:
            user = db.session.get(User, body_data["user_id"])
            if not user:
                return {"message": f"Invalid user_id: {body_data['user_id']}. User does not exist."}, 404
            order.user_id = body_data["user_id"]

        # Validate stock_id if provided
        if "stock_id" in body_data:
            stock = db.session.get(Stock, body_data["stock_id"])
            if not stock:
                return {"message": f"Invalid stock_id: {body_data['stock_id']}. Stock does not exist."}, 404
            order.stock_id = body_data["stock_id"]
            
            order.quantity=body_data.get("quantity") or order.quantity
            order.net_amount=body_data.get("net_amount") or order.net_amount    

            # commit changes
            db.session.commit()
            # return updated data
            return order_schema.dump(order), 200
        else:
            # if order doesn't exist
            return {"message": f"Order with id {order_id} does not exist"}, 404
    except ValueError: # invalide date format
        return {"message": "Invalid date format. Please use YYYY-MM-DD"}, 400   
    
# Delete - /orders/id - DELETE 
@orders_bp.route("/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    # find the order to delete using id
    stmt = db.select(Order).filter_by(id=order_id)
    order = db.session.scalar(stmt)
    if order:
        # delete
        db.session.delete(order)
        db.session.commit()
        # return response
        return {"message": f"Order with id'{order.id}' deleted successfully"}, 200
    else:
        # return error response
        return {"message": f"Order with id {order_id} does not exist"}, 404