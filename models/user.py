from init import db
from datetime import date

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(100), nullable=False)
    l_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    account_open_date = db.Column(db.Date, nullable=False, default=date.today)
    account_balance = db.Column(db.Decimal(precision=15, scale=2), nullable=False)

    orders = db.relationship("Order", back_populates = "user", cascade="all, delete-orphan")
    transactions = db.relationship("Transaction", back_populates = "user", cascade="all, delete-orphan")
    portfolios = db.relationship("Portfolio", back_populates = "user", cascade="all, delete-orphan")
    watchlists = db.relationship("Watchlist", back_populates = "user", cascade="all, delete-orphan")