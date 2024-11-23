from marshmallow import fields, post_dump

from init import ma
from enums import OrderType, OrderStatus

class OrderSchema(ma.Schema):
    class Meta:
        fields = ("id", "trade_date", "order_type", "quantity", "net_amount", "order_status", "user_id", "stock_id")

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