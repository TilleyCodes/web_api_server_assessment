from init import db
from datetime import date
from enums import OrderType, OrderStatus


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    trade_date = db.Column(db.Date, nullable=False, default=date.today)
    order_type = db.Column(db.Enum(OrderType), nullable=False) # this has enumerate
    quantity = db.Column(db.Integer, nullable=False)
    net_amount = db.Column(db.Numeric(precision=15, scale=2),nullable=False)
    order_status = db.Column(db.Enum(OrderStatus), nullable=False) # this has enumerate
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey("stocks.id"), nullable=False)
    #relationship  can have many orders to 1 user and 1 stock, 1 order to 1 transaction 
    user = db.relationship("User", back_populates= "orders")
    stock = db.relationship("Stock", back_populates = "orders") # dont need cascade delete as this refers to users and stocks table
    transaction = db.relationship("Transaction", back_populates = "order", cascade="all, delete-orphan")