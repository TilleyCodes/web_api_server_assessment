# pylint: disable=line-too-long

"""
This module defines the Order model representing orders placeds by investors in the database.
"""

from datetime import date

from init import db
from enums import OrderType, OrderStatus

class Order(db.Model):
    """
    This class represents an investor's order.
    """

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    trade_date = db.Column(db.Date, nullable=False, default=date.today)
    order_type = db.Column(db.Enum(OrderType), nullable=False) # this has enumerate
    quantity = db.Column(db.Integer, nullable=False)
    net_amount = db.Column(db.Numeric(precision=15, scale=2),nullable=False)
    order_status = db.Column(db.Enum(OrderStatus), nullable=False) # this has enumerate
    investor_id = db.Column(db.Integer, db.ForeignKey("investors.id"), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey("stocks.id"), nullable=False)
    #relationship  can have many orders to 1 investor and 1 stock, 1 order to 1 transaction
    investor = db.relationship("Investor", back_populates= "orders")
    stock = db.relationship("Stock", back_populates = "orders") # dont need cascade delete as this refers to investors and stocks table
    transaction = db.relationship("Transaction", back_populates = "order", cascade="all, delete-orphan")
