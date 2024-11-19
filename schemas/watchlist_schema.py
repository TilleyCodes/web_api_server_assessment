from init import ma

class WatchlistSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "stock_id")

watchlist_schema = WatchlistSchema()
watchlists_schema = WatchlistSchema(many=True)