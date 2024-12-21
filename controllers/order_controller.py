# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring


from datetime import date

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models import Order, Investor, Stock
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
            return {"message": "Request body is missing or contains invalid data"}, 400

        # validate & parse trade_date
        trade_date = (
            date.fromisoformat(body_data.get("trade_date"))
            if body_data.get("trade_date")
            else date.today()
        )
        # validate and convert order_type enum
        try:
            order_type = OrderType(body_data.get("order_type"))
        except ValueError:
            return{"message": f"Invalid order type. Please use one of the following: {[e.value for e in OrderType]}"}, 400

        # validate and convert order_status enum
        try:
            order_status = OrderStatus(body_data.get("order_status"))
        except ValueError:
            return{"message": f"Invalid order status. Please use one of the following: {[e.value for e in OrderStatus]}"}, 400

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
        quantity = body_data.get("quantity")
        if not isinstance(quantity, int) or quantity <=0:
            return {"message": "Quantity must be a numeric value and greater than 0."}, 400

        try:
            net_amount = float(body_data.get("net_amount"))
            if net_amount <= 0:
                return {"message": "Net amount must be greater than 0."}, 400
        except (ValueError, TypeError):
            return {"message": "Net amount must be a numeric value."}, 400

        # create order instance
        new_order = Order(
            trade_date=trade_date,
            order_type=order_type,
            quantity=quantity,
            net_amount=net_amount,
            order_status=order_status,
            investor_id=investor_id,
            stock_id=stock_id
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
    return {"message": "An unexpected error occurred."}, 500

# Read all - /orders - GET
@orders_bp.route("/", methods=["GET"])
def get_orders():
    stmt = db.select(Order)

    investor_id = request.args.get("investor_id")
    if investor_id:
        try:
            investor_id =int(investor_id) #validating investor id is a number and catching error
            stmt =stmt.filter(Order.investor_id==investor_id)
        except ValueError:
            return {"message": "Investor ID must be a number."}, 400

    stock_id = request.args.get("stock_id")
    if stock_id:
        try:
            stock_id = int(stock_id) #validating stock id is a number and catching error
            stmt =stmt.filter(Order.stock_id==stock_id)
        except ValueError:
            return {"message": "Stock ID must be a number."}, 400

    order_type = request.args.get("order_type")
    if order_type:
        try:
            valid_order_type = OrderType(order_type)  # check enum to validate order type
            stmt = stmt.filter(Order.order_type == valid_order_type)
        except ValueError:
            valid_values = [e.value for e in OrderType]
            return {"message": f"Invalid order_type. Valid values are: {valid_values}"}, 400

    order_status = request.args.get("order_status")
    if order_status:
        try:
            valid_order_status = OrderStatus(order_status)  # check enum to validate order status
            stmt = stmt.filter(Order.order_status == valid_order_status)
        except ValueError:
            valid_values = [e.value for e in OrderStatus]
            return {"message": f"Invalid order_status. Valid values are: {valid_values}"}, 400

    stmt =stmt.order_by(Order.id)
    orders_list = db.session.scalars(stmt).all()
    if not orders_list:
        return {"message": "No orders found with provided filters."}, 404
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
            return {"message": "Request body is missing or contains invalid data"}, 400

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
        # Validate investor_id if provided
        if "investor_id" in body_data:
            investor = db.session.get(Investor, body_data["investor_id"])
            if not investor:
                return {"message": f"Invalid investor_id: {body_data['investor_id']}. Investor does not exist."}, 404
            order.investor_id = body_data["investor_id"]

        # Validate stock_id if provided
        if "stock_id" in body_data:
            stock = db.session.get(Stock, body_data["stock_id"])
            if not stock:
                return {"message": f"Invalid stock_id: {body_data['stock_id']}. Stock does not exist."}, 404
            order.stock_id = body_data["stock_id"]

        # Validate and update quantity
        if "quantity" in body_data:
            if not isinstance(body_data["quantity"], int) or body_data["quantity"] <= 0:
                return {"message": "Quantity must be a numeric value and greater than 0."}, 400
            order.quantity = body_data["quantity"]

        # Validate and update net_amount
        if "net_amount" in body_data:
            try:
                net_amount = float(body_data.get("net_amount"))
                if net_amount <= 0:
                    return {"message": "Net amount must be greater than 0."}, 400
            except (ValueError, TypeError):
                return {"message": "Net amount must be a numeric value."}, 400

            # commit changes
            db.session.commit()
            # return updated data
            return order_schema.dump(order), 200

    except ValueError: #  date format
        return {"message": "Invalid date format. Please use YYYY-MM-DD"}, 400
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 400
        return {"message": "An unexpected error occurred."}, 500

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
        return {"message": f"Order with id' {order.id}' deleted successfully"}, 200
    else:
        # return error response
        return {"message": f"Order with id {order_id} does not exist"}, 404
    