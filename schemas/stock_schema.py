from init import ma

class StockSchema(ma.Schema):
    class Meta:
        fields = ("id", "stock_name", "ticker", "stock_price")

stock_schema = StockSchema()
stocks_schema = StockSchema(many=True)