# pylint: disable=line-too-long

"""
This module defines the schema for serialising and validating Investor objects.
"""

from datetime import date

from marshmallow import fields, validates
from marshmallow.exceptions import ValidationError

from init import ma

class InvestorSchema(ma.Schema):
    """
    This class validates and serialises Investor data.
    """
    ordered=True
    orders = fields.List(fields.Nested("OrderSchema", only=["trade_date", "order_type", "net_amount", "stock_id"], exclude=["investor", "stock"]))
    class Meta:
        """
        This class specifies fields for serialisation.
        """
        fields = ("id", "f_name", "l_name", "email", "registration_date", "account_balance", "orders")

    @validates('registration_date')
    def validate_registration_date(self, value):
        """
        This function ensures the registration date is not in the past.
        """
        today = date.today()
        if date.fromisoformat(value) < today:
            raise ValidationError("Registration date cannot be back dated.")

investor_schema = InvestorSchema()
investors_schema = InvestorSchema(many=True)
