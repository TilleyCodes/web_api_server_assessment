# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring

from marshmallow import fields

from init import ma

class InvestorSchema(ma.Schema):
    ordered=True
    orders = fields.List(fields.Nested("OrderSchema", only=["trade_date", "order_type", "net_amount", "stock_id"], exclude=["investor", "stock"]))
    class Meta:
        fields = ("id", "f_name", "l_name", "email", "registration_date", "account_balance", "orders")

investor_schema = InvestorSchema()
investors_schema = InvestorSchema(many=True)
