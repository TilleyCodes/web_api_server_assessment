from init import db
from models.user import User
from models.stock import Stock

class Watchlist(db.Model):
    __tablename__ = "watchlists"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey("stocks.id"), nullable=False)
    #relationship can have many watchlists but to 1 user and 1 stock
    user = db.relationship("User", back_populates="watchlists")
    stock = db.relationship("Stock", back_populates="watchlists")