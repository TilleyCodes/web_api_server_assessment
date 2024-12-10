# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring

from init import db

class Portfolio(db.Model):
    __tablename__ = "portfolios"

    id = db.Column(db.Integer, primary_key=True)
    number_of_units = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey("stocks.id"), nullable=False)
    # relationships can have many portfolios but to 1 user and 1 stock
    user = db.relationship("User", back_populates="portfolios")
    stock = db.relationship("Stock", back_populates="portfolios")
