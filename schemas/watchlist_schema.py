from init import ma

class WatchlistSchema(ma.Schema):
    class META:
        fields = ("id", "user_id", "stock_id")

watchlist_schema = WatchlistSchema()
watchlists_schema = WatchlistSchema(many=True)