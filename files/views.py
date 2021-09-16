
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from .models import User

views = Blueprint("views", __name__)

@views.route("/home")
@login_required
def home():
    users = User.query.all()
    return render_template("home.html", user=current_user, users=users)

"""
@views.route("/profile")
def profile():
    return render_template("profile.html")
"""
