from init import ma

class TransactionSchema(ma.Schema):
    class Meta:
        fields = ("id", "transaction_date", "transaction_type", "amount", "user_id", "order_id")

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)