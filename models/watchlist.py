from init import db

class Watchlist(db.Model):
    __tablename__ = "watchlists"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey("stocks.id"), nullable=False)
    #relationship
      # Relationships
    users = db.relationship("User", back_populates="watchlists")
    stocks = db.relationship("Stock", back_populates="watchlists")