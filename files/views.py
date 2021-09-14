
from flask import Blueprint, render_template, redirect, url_for

views = Blueprint("views", __name__)

@views.route("/")
def home_1():
    return redirect(url_for("views.home"))

@views.route("/home")
def home():
    return render_template("home.html")

@views.route("/profile")
def profile():
    return render_template("profile.html")
