from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):                               # The baseclass for all your models is called db.Model. It’s stored on the SQLAlchemy instance 
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())        # func gets the current date and time whenever a new obj is created
    # create foreign key to connect Note to User class
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):                    # https://stackoverflow.com/questions/63231163/what-is-the-usermixin-in-flask
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)      # no user can have the same email id
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')