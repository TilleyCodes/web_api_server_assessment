from marshmallow import fields

from init import ma

class StockSchema(ma.Schema):
    ordered=True
    orders = fields.List(fields.Nested("OrderSchema", exclude=["stock", "user"]))
    class Meta:
        fields = ("id", "stock_name", "ticker", "stock_price", "orders")

stock_schema = StockSchema()
stocks_schema = StockSchema(many=True)