"""
This Module schema for validating and serialising Portfolio data.
"""

from marshmallow import fields

from init import ma

class PortfolioSchema(ma.Schema):
    """
    This Class validates and serialises Portfolio data.
    """
    ordered=True
    investor = fields.Nested("InvestorSchema", only=["f_name", "l_name", "email"])
    stock = fields.Nested("StockSchema", only=["stock_name", "stock_price"])
    class Meta:
        """
        This class specifies fields for serialisation.
        """
        fields = ("id", "number_of_units", "investor_id", "investor", "stock_id", "stock")

portfolio_schema = PortfolioSchema()
portfolios_schema = PortfolioSchema(many=True)
