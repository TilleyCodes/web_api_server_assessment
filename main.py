import os
from flask import Flask
from init import db, ma

# basic app factories
def create_app():
    # initialising flask inside a function
    app = Flask(__name__)

    # provide details of the database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    # parsing flask app instance through a method called init_app
    db.init_app(app)
    ma.init_app(app)

    return app # flask app instance inside create_app function