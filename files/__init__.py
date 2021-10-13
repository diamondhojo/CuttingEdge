from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
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
    
    from .models import Employee

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Employee.query.get(int(id))

    return app

def create_database(app):
    if not path.exists("files/" + DB_NAME):
        db.create_all(app=app)
        # this gets all the column names
        conn = sqlite3.connect("files/database.db")
        cur = conn.cursor()
        password = generate_password_hash("password", method='sha256')

        #dummy data when creating new database (to be able to log in under new environment)
        cur.execute('INSERT INTO client(id, first_name, last_Name, email, address, date_created, date_updated) VALUES (1, \'Casey\', \'Damude\', \'casey.damude0232@hotmail.com\', \'8 Hamilton\', \'2021-10-04 18:38:54.501512\', \'2021-10-04 18:38:54.501512\')')
        cur.execute("INSERT INTO employee VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (1, 'Jordan', 'Race', 'diamondhojo@gmail.com', '4 Swan', password, 'Employee', '2021-10-04 18:38:54.501512', '2021-10-04 18:38:54.501512'))

        #Client column names
        cur.execute("SELECT * FROM client")
        views.clientCols = [tuple[0] for tuple in cur.description]

        #Employee column names
        cur.execute("SELECT * FROM employee")
        views.empCols = [tuple[0] for tuple in cur.description]

        conn.commit()
        conn.close()
        print("\nCreated database\n")
    else:
        print("\nDatabase already exists, using that one\n")
        conn = sqlite3.connect("files/database.db")
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT * FROM client")
            views.clientCols = [tuple[0] for tuple in cur.description]

            cur.execute("SELECT COUNT(*) FROM client")
            result = cur.fetchone()
            
            if result == '(0,)':
                print("\nNo clients found, inserting dummy data\n")
                cur.execute('INSERT INTO client(id, first_name, last_Name, email, address, date_created, date_updated) VALUES (1, \'Dummy\', \'Data\', \'DummyEmail@gmail.com\', \'DummyAddress\', \'2021-10-04 18:38:54.501512\', \'2021-10-04 18:38:54.501512\')')
            
            conn.commit()
        except:
            print("\nNo table such as 'client' exists. Creating table and inserting dummy data\n")
            cur.execute('CREATE TABLE client(id INT, first_name VARCHAR(50), last_name VARCHAR(50), email VARCHAR(100), address VARCHAR(100), date_created DATETIME, date_updated DATETIME);')
            cur.execute('INSERT INTO client(id, first_name, last_Name, email, address, date_created, date_updated) VALUES (1, \'Dummy\', \'Data\', \'DummyEmail@gmail.com\', \'DummyAddress\', \'2021-10-04 18:38:54.501512\', \'2021-10-04 18:38:54.501512\')')
            
            cur.execute("SELECT * FROM client")
            views.clientCols = [tuple[0] for tuple in cur.description]

            conn.commit()
        
        try:
            cur.execute("SELECT * FROM employee")
            views.empCols = [tuple[0] for tuple in cur.description]

            if cur.execute("SELECT COUNT(*) FROM employee") == 0:
                print("\nNo employees found, inserting dummy data\n")
                cur.execute('INSERT INTO employee(id, first_name, last_Name, email, address, password, position, date_created, date_updated) VALUES (1, \'DummyName\', \'DummyLastName\', \'Dummy@gmail.com\', \'Dummy\', \'Dummy\', password, \'Employee\', \'2021-10-04 18:38:54.501512\', \'2021-10-04 18:38:54.501512\')')

            conn.commit()
        except:
            print("\nNo table such as 'employee' exists. Creating table and inserting dummy data\n")
            
            cur.execute('CREATE TABLE employee(id INT, first_name VARCHAR(50), last_name VARCHAR(50), email VARCHAR(100), address VARCHAR(100), password VARCHAR(100), position VARCHAR(15), date_created DATETIME, date_updated DATETIME);')
            cur.execute('INSERT INTO employee(id, first_name, last_Name, email, address, password, position, date_created, date_updated) VALUES (1, \'Jordan\', \'Race\', \'diamondhojo@gmail.com\', \'PrisnMike\', \'4 Swan\', password, \'Employee\', \'2021-10-04 18:38:54.501512\', \'2021-10-04 18:38:54.501512\')')
            
            cur.execute("SELECT * FROM employee")
            views.empCols = [tuple[0] for tuple in cur.description]

            conn.commit()
        
        conn.close()