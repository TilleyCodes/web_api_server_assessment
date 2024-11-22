import os
from flask import Flask
from init import db, ma
from controllers.cli_controller import db_commands
from controllers.user_controller import users_bp
from controllers.stock_controller import stocks_bp

# basic app factories
def create_app():
    # initialising flask inside a function
    app = Flask(__name__)
   
    # provide details of the database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    # parsing flask app instance through a method called init_app
    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(db_commands) #register blueprint from cli_controller
    app.register_blueprint(users_bp)
    app.register_blueprint(stocks_bp)

    return app # flask app instance inside create_app function