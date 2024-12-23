# pylint: disable=line-too-long

"""
This module defines the Portfolio model representing stock holdings of investors.
"""

from init import db

class Portfolio(db.Model):
    """
    This classepresents an investor's portfolio, detailing stock holdings.
    """

    __tablename__ = "portfolios"

    id = db.Column(db.Integer, primary_key=True)
    number_of_units = db.Column(db.Integer, nullable=False)
    investor_id = db.Column(db.Integer, db.ForeignKey("investors.id"), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey("stocks.id"), nullable=False)
    # relationships can have many portfolios but to 1 investor and 1 stock
    investor = db.relationship("Investor", back_populates="portfolios")
    stock = db.relationship("Stock", back_populates="portfolios")
