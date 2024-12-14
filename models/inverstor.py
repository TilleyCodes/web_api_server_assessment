# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring

from datetime import date

from init import db

class Investor(db.Model):
    __tablename__ = "investors"

    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(100), nullable=False)
    l_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    registration_date = db.Column(db.Date, nullable=False, default=date.today)
    account_balance = db.Column(db.Numeric(precision=15, scale=2), nullable=False)
    #relationship 1 investor can have many
    orders = db.relationship("Order", back_populates = "investor", cascade="all, delete-orphan")
    transactions = db.relationship("Transaction", back_populates = "investor", cascade="all, delete-orphan")
    portfolios = db.relationship("Portfolio", back_populates = "investor", cascade="all, delete-orphan")
    watchlists = db.relationship("Watchlist", back_populates = "investor", cascade="all, delete-orphan")
