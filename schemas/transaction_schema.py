from marshmallow import fields, post_dump

from init import ma
from enums import TransactionType

class TransactionSchema(ma.Schema):
    class Meta:
        fields = ("id", "transaction_date", "transaction_type", "amount", "user_id", "order_id")

    @post_dump
    def serialize_enum(self, data, **kwargs):
        # Convert enum fields to their string representations
        if isinstance(data.get("transaction_type"), TransactionType):
            data["transaction_type"] = data["transaction_type"].value
        return data

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)