# pylint: disable=missing-module-docstring

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# initialising sqlalchemy and marshmallow
db = SQLAlchemy()
ma = Marshmallow()
