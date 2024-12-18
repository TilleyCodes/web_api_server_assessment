# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring

from init import db

class Stock(db.Model):
    __tablename__ = "stocks"

    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String(100), nullable=False, unique=True)
    ticker = db.Column(db.String(100), nullable=False, unique=True)
    stock_price = db.Column(db.Numeric(precision=15, scale=2),nullable=False, check=db.CheckConstraint("stock_price >= 0"))
    # Relationship 1 stock can have many. Need to have cascade as it is referenced to other tables
    orders = db.relationship("Order", back_populates = "stock", cascade="all, delete-orphan")
    portfolios = db.relationship("Portfolio", back_populates = "stock", cascade="all, delete-orphan")
    watchlists = db.relationship("Watchlist", back_populates = "stock", cascade="all, delete-orphan")
