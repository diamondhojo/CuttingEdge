from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from . import views
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
@auth.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('No account is associated with the given email address.', category='error')
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@auth.route("/signup", methods=['GET', 'POST'])
def sign_up():
    #removing unnecessary columns that don't need user input
    signupcols = cols
    if signupcols.__contains__("id"):
        signupcols.remove("id")
    if signupcols.__contains__("password"):
        signupcols.remove("password")
    if signupcols.__contains__("employee"):
        signupcols.remove("employee")
    if signupcols.__contains__("user_type"):
        signupcols.remove("user_type")
    if signupcols.__contains__("date_created"):
        signupcols.remove("date_created")
    if signupcols.__contains__("date_updated"):
        signupcols.remove("date_updated")

    if request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        address = request.form.get("address")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user_type = str(request.form.get("user_type"))

        email_exists = User.query.filter_by(email=email).first()
        address_exists = User.query.filter_by(address=address).first()
        username_exists = User.query.filter_by(username=username).first()
        name_exists = User.query.filter_by(first_name=first_name, last_name=last_name).first()

        if name_exists:
            flash('Name combination is already in use.', category='error')
        elif len(first_name) < 3:
            flash('First name must be at least 3 characters long.', category='error')
        elif len(last_name) < 3:
            flash('Last name must be at least 3 characters long.', category='error')
        elif email_exists:
            flash('Email is already in use.', category='error')
        elif address_exists:
            flash('Address is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif password1 != password2:
            flash('Password don\'t match!', category='error')
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
        elif len(password1) < 6:
            flash('Password is too short.', category='error')

        else:
            new_user = User(first_name=first_name, last_name=last_name, email=email, address=address, username=username, password=generate_password_hash(password1, method='sha256'), user_type=user_type, date_created=datetime.now(), date_updated=datetime.now())
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user, signupcols=signupcols)
