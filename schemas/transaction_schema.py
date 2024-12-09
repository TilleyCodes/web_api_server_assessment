# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=unused-import
 # pylint: disable=unused-argument


from marshmallow import fields, post_dump
# need to take a look at fields - unused-import disable

from init import ma
from enums import TransactionType

class TransactionSchema(ma.Schema):
    ordered=True
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
