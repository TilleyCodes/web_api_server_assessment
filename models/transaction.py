from init import db
from datetime import date

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.Date, nullable=False, default=date.today)
    transaction_type = db.Column(db.String(100), nullable=False) # this has enumerate
    amount = db.Column(db.Decimal(precision=15, scale=2),nullable=False)
    # user_id =
    # order_id =