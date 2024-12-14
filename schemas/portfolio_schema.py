# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring

from init import ma

class PortfolioSchema(ma.Schema):
    ordered=True
    class Meta:
        fields = ("id", "number_of_units", "investor_id", "stock_id")

portfolio_schema = PortfolioSchema()
portfolios_schema = PortfolioSchema(many=True)
