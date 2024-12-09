# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import os

from flask import Flask

from init import db, ma
from controllers import db_commands, users_bp, stocks_bp, orders_bp, transactions_bp, portfolios_bp, watchlists_bp
# from controllers.cli_controller import db_commands
# from controllers.user_controller import users_bp
# from controllers.stock_controller import stocks_bp

# basic app factories
def create_app():
    # initialising flask inside a function
    app = Flask(__name__)

    # provide details of the database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    app.json.sort_keys = False # to stop json from sorting by keys and sort by order in marshmallow

    # parsing flask app instance through a method called init_app
    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(db_commands) #register blueprint from cli_controller
    app.register_blueprint(users_bp)
    app.register_blueprint(stocks_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(portfolios_bp)
    app.register_blueprint(watchlists_bp)

    return app # flask app instance inside create_app function
