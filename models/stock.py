# pylint: disable=line-too-long

"""
this module defines the Stock model representing stocks in the database.
"""

from init import db

class Stock(db.Model):
    """
    This class represents a stock with its details and relationships.
    """
    __tablename__ = "stocks"

    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String(100), nullable=False, unique=True)
    ticker = db.Column(db.String(100), nullable=False, unique=True)
    stock_price = db.Column(db.Numeric(precision=15, scale=2),nullable=False)
    # Relationship 1 stock can have many. Need to have cascade as it is referenced to other tables
    orders = db.relationship("Order", back_populates = "stock", cascade="all, delete-orphan")
    portfolios = db.relationship("Portfolio", back_populates = "stock", cascade="all, delete-orphan")
    watchlists = db.relationship("Watchlist", back_populates = "stock", cascade="all, delete-orphan")
