# pylint: disable=line-too-long

"""
This Module schema for validating and serialising Stock data.
"""

from marshmallow import fields

from init import ma

class StockSchema(ma.Schema):
    """
    This Class validates and serialises Stock data.
    """
    ordered=True
    orders = fields.List(fields.Nested("OrderSchema", only=["order_type", "quantity"], exclude=["stock", "investor"]))
    class Meta:
        """
        This class specifies fields for serialisation.
        """
        fields = ("id", "stock_name", "ticker", "stock_price", "orders")

stock_schema = StockSchema()
stocks_schema = StockSchema(many=True)
