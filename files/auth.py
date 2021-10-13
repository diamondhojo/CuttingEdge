from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from . import db
from . import views
from .models import Employee, Client
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
@auth.route("/", methods=['GET', 'POST'])
def login():
    info = ""
    clients = Client.query.all()
    clientCols = views.GetCols("Client")

    if clientCols.__contains__("id"):
        clientCols.remove("id")
    if clientCols.__contains__("date_updated"):
        clientCols.remove("date_updated")
    
    if current_user.is_authenticated:
        return render_template("clients.html", employee = current_user, clients=clients, clientCols=clientCols)        

    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        #email = 'diamondhojo@gmail.com'
        #password = 'password'
        employee = Employee.query.filter_by(email=email).first()

        if employee:
            if check_password_hash(employee.password, password):
                login_user(employee, remember=True)
                return redirect(url_for('views.clients'))
            else:
                info = email
                flash('Password is incorrect.', category='error')
        else:
            flash('No account is associated with the given email address.', category='error')
    
    return render_template("login.html", employee=current_user, info=info)
    

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
