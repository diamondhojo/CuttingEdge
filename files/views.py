
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
import sqlite3
from sqlite3 import dbapi2 as sqlite
import string
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from . import auth

views = Blueprint("views", __name__)

@views.route("/home")
@login_required
def home():
    users = User.query.all()
    user = current_user
    return render_template("home.html", user=current_user, users=users, cols=auth.cols)

@views.route("/profile/<username>")
def profile(username):
    user = current_user
    return render_template("profile.html", username=user.username, user=user)

@views.route("/newUser", methods=['GET', 'POST'])
@login_required
def newUser():
    users = User.query.all()
    if request.method == 'POST':
        first_name = request.form.get("First_Name")
        last_name = request.form.get("Last_Name")
        email = request.form.get("Email")
        address = request.form.get("Address")
        username = request.form.get("Username")
        password1 = "123456"
        password2 = "123456"

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
            new_user = User(first_name=first_name, last_name=last_name, email=email, address=address, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('User Created')
            return redirect(url_for('views.home'))

    return render_template("newUser.html", user=current_user, users=users, cols=auth.cols)


@views.route("/delete/<id>")
@login_required
def delete(id):
    user = User.query.filter_by(id=id).first()
    
    if not user:
        flash("User doesn't exist", category='error')
    else:
        db.session.delete(user)
        db.session.commit()
        flash(current_user.is_authenticated)
        flash("User deleted", category='success')
        return redirect(url_for('views.home'))
        
    
