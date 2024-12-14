# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring

from init import db

class Watchlist(db.Model):
    __tablename__ = "watchlists"

    id = db.Column(db.Integer, primary_key=True)
    investor_id = db.Column(db.Integer, db.ForeignKey("investors.id"), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey("stocks.id"), nullable=False)
    #relationship can have many watchlists but to 1 investor and 1 stock
    investor = db.relationship("Investor", back_populates="watchlists")
    stock = db.relationship("Stock", back_populates="watchlists")
