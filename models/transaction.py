from init import db
from datetime import date
from enums import TransactionType

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.Date, nullable=False, default=date.today)
    transaction_type = db.Column(db.Enum(TransactionType), nullable=False) # this has enumerate
    amount = db.Column(db.Numeric(precision=15, scale=2),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    # relationships can have many transactions but to 1 user and order
    users = db.relationship("User", back_populates="transactions")
    order = db.relationship("Order", back_populates="transactions")