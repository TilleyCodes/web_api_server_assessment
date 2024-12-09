from init import ma

class UserSchema(ma.Schema):
    ordered=True
    orders = fields.List(fields.Nested("OrderSchema", only=["trade_date", "order_type", "net_amount", "stock_id"], exclude=["user", "stock"]))
    class Meta:
        fields = ("id", "f_name", "l_name", "email", "account_open_date", "account_balance", "orders")

user_schema = UserSchema()
users_schema = UserSchema(many=True)
