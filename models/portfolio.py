from init import db

class Portfolio(db.Model):
    __tablename__ = "portfolios"

    id = db.Column(db.Integer, primary_key=True)
    number_of_units = db.Column(db.Integer, nullable=False)
    # user_id = 
    # stock_id =