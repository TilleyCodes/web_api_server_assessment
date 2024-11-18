from init import ma

class UserSchema(ma.Schema):
    class META:
        fields = ("id", "f_name", "l_name", "email", "account_open_date", "account_balance")

user_schema = UserSchema()
users_schema = UserSchema(many=True)