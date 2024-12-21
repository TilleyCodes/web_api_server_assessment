"""
This module schema for validating and serialising Watchlist data.
"""

from marshmallow import fields

from init import ma

class WatchlistSchema(ma.Schema):
    """
    This class validates and serialises Watchlist data.
    """
    ordered=True
    investor = fields.Nested("InvestorSchema", only=["f_name", "l_name", "email"])
    stock = fields.Nested("StockSchema", only=["stock_name", "stock_price"])
    class Meta:
        """
        This class specifies fields for serialisation.
        """
        fields = ("id", "investor_id", "investor", "stock_id", "stock")

watchlist_schema = WatchlistSchema()
watchlists_schema = WatchlistSchema(many=True)
