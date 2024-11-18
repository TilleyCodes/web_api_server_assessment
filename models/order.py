from init import db
from datetime import date

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    trade_date = db.Column(db.Date, nullable=False, default=date.today)
    order_type = db.Column(db.String(100), nullable=False) # this has enumerate
    quantity = db.Column(db.Integer, nullable=False)
    net_amount = db.Column(db.Decimal(precision=15, scale=2),nullable=False)
    status = db.Column(db.String(100), nullable=False) # this has enumerate
    # user_id = 
    # stock_id =