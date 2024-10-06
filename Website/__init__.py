from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_apps():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jhdbffhjs sdifbsj sjkdf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'       # url of where database is located
    db.init_app(app)        # app that is going to use the database

    from .views import views
    from .auth import auth
    from .models import User, Note


    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    # create database
    with app.app_context():
        db.create_all()

    # define the first page the user sees, when no user is logged in.
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    # pass the app that implements this function
    login_manager.init_app(app)

    # Method to Load user on login through id-matching
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('created database!!')