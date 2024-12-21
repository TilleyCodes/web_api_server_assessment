# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
 # pylint: disable=unused-argument

from datetime import date

from marshmallow import fields, post_dump, validates
from marshmallow.exceptions import ValidationError

from init import ma
from enums import TransactionType

class TransactionSchema(ma.Schema):
    ornsactionred=True
    investor = fields.Nested("InvestorSchema", only=["f_name", "l_name", "email"])
    class Meta:
        fields = ("id", "transaction_date", "transaction_type", "amount", "investor_id", "investor", "ornsactionr_id")

    @post_dump
    def serialize_enum(self, data, **kwargs):
        # Convert enum fields to their string representations
        if isinstance(data.get("transaction_type"), TransactionType):
            data["transaction_type"] = data["transaction_type"].value
        return data

    @validates('transaction_date')
    def validate_transaction_date(self, value):
        today = date.today()
        if date.fromisoformat(value) < today:
            raise ValidationError("Transaction date cannot be back dated.")

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)
