"""
This module defines the Watchlist model for tracking stocks that investors are monitoring.
"""
from init import db

class Watchlist(db.Model):
    """
    This class represents a stock watchlist entry for an investor.
    """
    __tablename__ = "watchlists"

    id = db.Column(db.Integer, primary_key=True)
    investor_id = db.Column(db.Integer, db.ForeignKey("investors.id"), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey("stocks.id"), nullable=False)
    #relationship can have many watchlists but to 1 investor and 1 stock
    investor = db.relationship("Investor", back_populates="watchlists")
    stock = db.relationship("Stock", back_populates="watchlists")
