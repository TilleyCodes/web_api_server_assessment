from init import ma

class OrderSchema(ma.Schema):
    class Meta:
        fields = ("id", "trade_date", "order_type", "quantity", "net_amount", "order_status", "user_id", "stock_id")

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)