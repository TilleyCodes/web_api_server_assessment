from init import ma
from enums import OrderType, OrderStatus

class OrderSchema(ma.Schema):
    ordered=True
    user = fields.Nested("UserSchema", only=["f_name", "l_name", "email", "account_balance"])
    stock = fields.Nested("StockSchema", only=["stock_name", "stock_price"])
    class Meta:
        fields = ("id", "trade_date", "order_type", "quantity", "net_amount", "order_status", "user_id", "user", "stock_id", "stock" )

    @post_dump
    def serialize_enum(self, data, **kwargs):
        # Convert enum fields to their string representations
        if isinstance(data.get("order_status"), OrderStatus):
            data["order_status"] = data["order_status"].value
        if isinstance(data.get("order_type"), OrderType):
            data["order_type"] = data["order_type"].value
        return data

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
