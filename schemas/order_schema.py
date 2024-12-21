# pylint: disable=line-too-long
# pylint: disable=unused-argument

"""
This module schema for validating and serialising Order data.
"""

from datetime import date

from marshmallow import fields, post_dump, validates
from marshmallow.exceptions import ValidationError

from init import ma
from enums import OrderType, OrderStatus

class OrderSchema(ma.Schema):
    """
    This class validates and serialises Order data.
    """
    ordered=True
    investor = fields.Nested("InvestorSchema", only=["f_name", "l_name", "email", "account_balance"])
    stock = fields.Nested("StockSchema", only=["stock_name", "stock_price"])
    class Meta:
        """
        This class specifies fields for serialisation.
        """
        fields = ("id", "trade_date", "order_type", "quantity", "net_amount", "order_status", "investor_id", "investor", "stock_id", "stock" )

    @post_dump
    def serialize_enum(self, data, **kwargs):
        """
        This function converts enum fields to string representations.
        """
        if isinstance(data.get("order_status"), OrderStatus):
            data["order_status"] = data["order_status"].value
        if isinstance(data.get("order_type"), OrderType):
            data["order_type"] = data["order_type"].value
        return data

    @validates('trade_date')
    def validate_trade_date(self, value):
        """
        This function validates that the trade date is not in the past.
        """
        today = date.today()
        if date.fromisoformat(value) < today:
            raise ValidationError("Trade date cannot be back dated.")

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
