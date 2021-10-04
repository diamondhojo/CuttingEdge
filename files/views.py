
from datetime import datetime
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
    
    #keeping column names up to date (without it, after signing up (from deleted database), creating a new user from the homepage, after saving, homepage returns with fewer column names)
    conn = sqlite3.connect("files/database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM User")
    homecols = [tuple[0] for tuple in cur.description]
    conn.close()

    if homecols.__contains__("id"):
        homecols.remove("id")
    if homecols.__contains__("password"):
        homecols.remove("password")
    if homecols.__contains__("date_updated"):
        homecols.remove("date_updated")

    return render_template("home.html", user=current_user, users=users, homecols=homecols)

@views.route("/profile/<username>", methods=['GET', 'POST'])
def profile(username):
    user = User.query.filter_by(username=username).first()
    profilecols = cols
    
    if profilecols.__contains__("id"):
        profilecols.remove("id")
    if profilecols.__contains__("password"):
        profilecols.remove("password")

    if request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        address = request.form.get("address")
        username = request.form.get("username")
        if user == current_user:
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")
        errors = False
               
        if user.first_name != first_name or user.last_name != last_name:
            name_exists = User.query.filter_by(first_name=first_name, last_name=last_name).first()
            if name_exists:
                flash('Name combination is already in use.', category='error')
                errors = True
            else:
                if len(first_name) < 3:
                    flash('First name must be at least 3 characters long.', category='error')
                    errors = True
                elif len(last_name) < 3:
                    flash('Last name must be at least 3 characters long.', category='error')
                    errors = True
                else:
                    user.first_name = first_name.title()
                    user.last_name = last_name.title()

        if user.email != email:
            email_exists = User.query.filter_by(email=email).first()
            if email_exists:
                flash('Email is already in use.', category='error')
                errors = True
            else:
                if  (len(email) < 8) or "@" not in email or "." not in email:
                    flash("Email is invalid.", category='error')
                    errors = True
                else:
                    user.email = email

        if user.address != address:
            address_exists = User.query.filter_by(address=address).first()
            if address_exists:
                flash('Address is already in use.', category='error')
                errors = True
            else:
                user.first_name = first_name

        if user.username != username:
            username_exists = User.query.filter_by(username=username).first()
            if username_exists:
                flash('Username is already in use.', category='error')
                errors = True
            else:
                if len(username) < 2:
                    flash('Username is too short.', category='error')
                    errors = True
                else:
                    user.username = username
    
        if password1 != "" and password2 != "":
            if len(password1) < 6:
                flash('Password is too short.', category='error')
                errors = True
            elif len(password2) < 6:
                flash('Password is too short.', category='error')
                errors = True
            elif password1 == password2:
                flash('Passwords don\'t match.', category='error')
                errors = True
            else:
                user.password = generate_password_hash(password1, method='sha256')
                flash('Password changed', category='success')

        if errors == False:
            user.date_updated = datetime.now()
            db.session.commit()
            return redirect(url_for('views.home'))

    return render_template("profile.html", current_user=current_user, user=user, profilecols=profilecols)

@views.route("/newUser", methods=['GET', 'POST'])
@login_required
def newUser():
    users = User.query.all()

    newusercols = cols
    if newusercols.__contains__("id"):
        newusercols.remove("id")
    if newusercols.__contains__("password"):
        newusercols.remove("password")
    if newusercols.__contains__("user_type"):
        newusercols.remove("user_type")
    if newusercols.__contains__("date_created"):
        newusercols.remove("date_created")
    if newusercols.__contains__("date_updated"):
        newusercols.remove("date_updated")

    if request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        address = request.form.get("address")
        username = request.form.get("username")
        password = "password"
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
        else:
            new_user = User(first_name=first_name, last_name=last_name, email=email, address=address, username=username, password=generate_password_hash(password, method='sha256'), user_type=user_type, date_created=datetime.now(), date_updated=datetime.now())
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('views.home'))

    return render_template("newUser.html", user=current_user, users=users, newusercols=newusercols)


@views.route("/delete/<username>")
@login_required
def delete(username):
    user = User.query.filter_by(username=username).first()
    
    if not user:
        flash("User doesn't exist", category='error')
    else:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('views.home'))
        
    
