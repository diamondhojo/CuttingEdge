from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import sqlite3

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists("files/" + DB_NAME):
        db.create_all(app=app)
        # this gets all the column names
        conn = sqlite3.connect("files/database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM User")
        auth.cols = [tuple[0] for tuple in cur.description]
        print(auth.cols)
        print("\n\n")
        views.cols = [tuple[0] for tuple in cur.description]
        print(views.cols)
        print("\n\n")
        conn.close()
        print("\nCreated database\n")
    else:
        conn = sqlite3.connect("files/database.db")
        cur = conn.cursor()
        print("\nDatabase already exists, using that one\n")
        try:
            cur.execute("SELECT * FROM User")
            auth.cols = [tuple[0] for tuple in cur.description]
            print(auth.cols)
            print("\n\n")
            views.cols = [tuple[0] for tuple in cur.description]
            print(views.cols)
            print("\n\n")
            conn.close()
        except:
            print("\nDatabase does exist, though no table such as 'Users' exist. Creating table called 'Users'\n")
            cur.execute('CREATE TABLE User(id INT, first_name VARCHAR(50), last_name VARCHAR(50), email VARCHAR(100), username VARCHAR(100), address VARCHAR(100), password VARCHAR(100), date_created DATETIME, date_updated DATETIME);')
            cur.execute("SELECT * FROM User")
            auth.cols = [tuple[0] for tuple in cur.description]
            print(auth.cols)
            print("\n\n")
            views.cols = [tuple[0] for tuple in cur.description]
            print(views.cols)
            print("\n\n")
            conn.close()
