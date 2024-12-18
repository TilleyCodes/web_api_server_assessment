# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring

from marshmallow import fields

from init import ma

class WatchlistSchema(ma.Schema):
    ordered=True
    investor = fields.Nested("InvestorSchema", only=["f_name", "l_name", "email"])
    stock = fields.Nested("StockSchema", only=["stock_name", "stock_price"])
    class Meta:
        fields = ("id", "investor_id", "investor", "stock_id", "stock")

watchlist_schema = WatchlistSchema()
watchlists_schema = WatchlistSchema(many=True)
