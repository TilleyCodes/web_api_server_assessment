# pylint: disable=line-too-long

"""
This module defines the Transaction model for tracking financial transactions of investors.
"""

from datetime import date

from init import db
from enums import TransactionType

class Transaction(db.Model):
    """
    This class represents a transaction between an investor.
    """
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.Date, nullable=False, default=date.today)
    transaction_type = db.Column(db.Enum(TransactionType), nullable=False) # this has enumerate
    amount = db.Column(db.Numeric(precision=15, scale=2),nullable=False)
    investor_id = db.Column(db.Integer, db.ForeignKey("investors.id"), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=True)
    # relationships can have many transactions but to 1 investor and order
    investor = db.relationship("Investor", back_populates="transactions")
    order = db.relationship("Order", back_populates="transaction")
