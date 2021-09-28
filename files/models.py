
from . import db    # . represents the current working dir, db references the db variable in init.py
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    address = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
