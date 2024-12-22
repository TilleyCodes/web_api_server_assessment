# pylint: disable=line-too-long
# pylint: disable=unused-argument

"""
This Module schema for validating and serialising Transaction data.
"""

from datetime import date

from marshmallow import fields, post_dump, validates
from marshmallow.exceptions import ValidationError

from init import ma
from enums import TransactionType

class TransactionSchema(ma.Schema):
    """
    This class validates and serialises Transaction data.
    """
    ordered=True
    investor = fields.Nested("InvestorSchema", only=["f_name", "l_name", "email"])
    class Meta:
        """
        This class specifies fields for serialisation.
        """
        fields = ("id", "transaction_date", "transaction_type", "amount", "investor_id", "investor", "order_id")

    @post_dump
    def serialize_enum(self, data, **kwargs):
        """
        This function converts enum fields to string representations.
        """
        if isinstance(data.get("transaction_type"), TransactionType):
            data["transaction_type"] = data["transaction_type"].value
        return data

    @validates('transaction_date')
    def validate_transaction_date(self, value):
        """
        this function ensures the transaction date is not in the past.
        """
        today = date.today()
        if date.fromisoformat(value) < today:
            raise ValidationError("Transaction date cannot be back dated.")

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)
