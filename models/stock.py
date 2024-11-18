from init import db

class Stock(db.Model):
    __tablename__ = "stocks"

    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String(100), nullable=False)
    ticker = db.Column(db.String(100), nullable=False)
    stock_price = db.Column(db.Decimal(precision=15, scale=2),nullable=False)

    orders = db.relationship("Order", back_populates = "stock", cascade="all, delete-orphan")
    portfolios = db.relationship("Portfolio", back_populates = "stock", cascade="all, delete-orphan")
    watchlists = db.relationship("Watchlist", back_populates = "stock", cascade="all, delete-orphan")