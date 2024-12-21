# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from datetime import date

from marshmallow import fields, validates
from marshmallow.exceptions import ValidationError

from init import ma

class InvestorSchema(ma.Schema):
    ordered=True
    orders = fields.List(fields.Nested("OrderSchema", only=["trade_date", "order_type", "net_amount", "stock_id"], exclude=["investor", "stock"]))
    class Meta:
        fields = ("id", "f_name", "l_name", "email", "registration_date", "account_balance", "orders")

    @validates('registration_date')
    def validate_registration_date(self, value):
        today = date.today()
        if date.fromisoformat(value) < today:
            raise ValidationError("Registration date cannot be back dated.")

investor_schema = InvestorSchema()
investors_schema = InvestorSchema(many=True)
