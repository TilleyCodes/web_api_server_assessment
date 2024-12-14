# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring

from init import ma

class WatchlistSchema(ma.Schema):
    ordered=True
    class Meta:
        fields = ("id", "investor_id", "stock_id")

watchlist_schema = WatchlistSchema()
watchlists_schema = WatchlistSchema(many=True)
