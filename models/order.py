from init import db
from datetime import date
from enums import OrderType, OrderStatus


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    trade_date = db.Column(db.Date, nullable=False, default=date.today)
    order_type = db.Column(db.Enum(OrderType), nullable=False) # this has enumerate
    quantity = db.Column(db.Integer, nullable=False)
    net_amount = db.Column(db.Decimal(precision=15, scale=2),nullable=False)
    order_status = db.Column(db.Enum(OrderStatus), nullable=False) # this has enumerate
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey("stocks.id"), nullable=False)
    #relationship with transactions
    users = db.relationship("User", back_populates= "order", cascade="all, delete-orphan")
    transactions = db.relationship("Transaction", back_populates = "order", cascade="all, delete-orphan")