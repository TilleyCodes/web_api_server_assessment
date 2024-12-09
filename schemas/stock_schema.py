from init import ma

class StockSchema(ma.Schema):
    ordered=True
    orders = fields.List(fields.Nested("OrderSchema", only=["order_type", "quantity"], exclude=["stock", "user"]))
    class Meta:
        fields = ("id", "stock_name", "ticker", "stock_price", "orders")

stock_schema = StockSchema()
stocks_schema = StockSchema(many=True)
