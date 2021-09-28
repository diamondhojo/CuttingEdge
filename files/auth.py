from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from . import views
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

auth = Blueprint("auth", __name__)

# this gets all the column names
conn = sqlite3.connect("files/database.db")
cur = conn.cursor()
cur.execute("SELECT * FROM User")
cols = [tuple[0] for tuple in cur.description]
cols.remove('id')
cols.remove('date_created')
cols.remove('password')
conn.close()
# capitalizes each word of each string (list item) in all_cols
cols = [col.title() for col in cols]

def updateDB(first_name, last_name, email, address, username, password):
    new_user = User(first_name=first_name, last_name=last_name, email=email, address=address, username=username, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    current_user = new_user
    if not current_user.is_authenticated:
        login_user(new_user, remember=True)
        if current_user.is_authenticated:
            flash("Logging in")
        else:
            flash("Logged out")
    else:
        flash("logged in")
    return flash('User Created')

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
    if request.method == 'POST':
        first_name = request.form.get("First_Name")
        last_name = request.form.get("Last_Name")
        email = request.form.get("Email")
        address = request.form.get("Address")
        username = request.form.get("Username")
        password1 = request.form.get("Username")
        password2 = request.form.get("Username")

        flash(first_name, category='success')

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
            login_user(new_user, remember=True)
            flash('User Created and Logged In')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user, cols=cols)
