
from datetime import datetime
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from sqlite3 import dbapi2 as sqlite
import string, json, sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Client, Employee
from . import db, auth

views = Blueprint("views", __name__)
cols = []

def GetCols(model):
    conn = sqlite3.connect("files/database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + model)
    info = [tuple[0] for tuple in cur.description]
    conn.close()
    return info

"""
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
                                CLIENTS
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
"""
@views.route("/clients", methods=['GET', 'POST'])
def clients():
    clients = Client.query.all()
    clientCols = GetCols("Client")

    if clientCols.__contains__("id"):
        clientCols.remove("id")
    if clientCols.__contains__("date_updated"):
        clientCols.remove("date_updated")

    return render_template("clients.html", employee=current_user, clients=clients, clientCols=clientCols)

@views.route("/edit-client/<id>", methods=['GET', 'POST'])
def editClient(id):
    client = Client.query.filter_by(id=id).first()
    clientCols = GetCols("Client")
    
    if clientCols.__contains__("id"):
        clientCols.remove("id")
    if clientCols.__contains__("password"):
        clientCols.remove("password")

    if request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        address = request.form.get("address")
        errors = False
               
        if client.first_name != first_name or client.last_name != last_name:
            name_exists = Client.query.filter_by(first_name=first_name, last_name=last_name).first()
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
                    client.first_name = first_name.title()
                    client.last_name = last_name.title()

        if client.email != email:
            email_exists = client.query.filter_by(email=email).first()
            if email_exists:
                flash('Email is already in use.', category='error')
                errors = True
            else:
                if  (len(email) < 8) or "@" not in email or "." not in email:
                    flash("Email is invalid.", category='error')
                    errors = True
                else:
                    client.email = email

        if client.address != address:
            address_exists = Client.query.filter_by(address=address).first()
            if address_exists:
                flash('Address is already in use.', category='error')
                errors = True
            else:
                client.first_name = first_name

        if errors == False:
            client.date_updated = datetime.now()
            db.session.commit()
            return redirect(url_for('views.clients'))

    return render_template("editClient.html", employee=current_user, client=client, clientCols=clientCols)

@views.route("/new-client", methods=['GET', 'POST'])
@login_required
def newClient():
    clients = Client.query.all()
    clientCols = GetCols("Client")

    if clientCols.__contains__("id"):
        clientCols.remove("id")
    if clientCols.__contains__("date_created"):
        clientCols.remove("date_created")
    if clientCols.__contains__("date_updated"):
        clientCols.remove("date_updated")

    if request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        address = request.form.get("address")

        email_exists = Client.query.filter_by(email=email).first()
        address_exists = Client.query.filter_by(address=address).first()
        name_exists = Client.query.filter_by(first_name=first_name, last_name=last_name).first()
        
        if name_exists:
            flash('Name combination is already in use.', category='error')
        elif len(first_name) < 3:
            flash('First name must be at least 3 characters long.', category='error')
        elif len(last_name) < 3:
            flash('Last name must be at least 3 characters long.', category='error')
        elif email_exists:
            flash('Email is already in use.', category='error')
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
        elif address_exists:
            flash('Address is already in use.', category='error')
        else:
            new_client = Client(first_name=first_name, last_name=last_name, email=email, address=address, date_created=datetime.now(), date_updated=datetime.now())
            db.session.add(new_client)
            db.session.commit()
            return redirect(url_for('views.clients'))

    return render_template("newClient.html", employee=current_user, clients=clients, clientCols=clientCols)





"""
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
                                EMPLOYEES
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
"""
@views.route("/employees")
@login_required
def employees():
    employees = Employee.query.all()
    employee = current_user
    empCols = GetCols("Employee")

    if empCols.__contains__("id"):
        empCols.remove("id")
    if empCols.__contains__("password"):
        empCols.remove("password")
    if empCols.__contains__("date_updated"):
        empCols.remove("date_updated")

    return render_template("employees.html", employee=current_user, employees=employees, empCols=empCols)

@views.route("/edit-employee/<id>", methods=['GET', 'POST'])
def editEmployee(id):
    employee = Employee.query.filter_by(id=id).first()
    empCols = GetCols("Employee")
    
    if empCols.__contains__("id"):
        empCols.remove("id")

    if request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        address = request.form.get("address")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        position = request.form.get("position")
        errors = False
               
        if employee.first_name != first_name or employee.last_name != last_name:
            name_exists = Employee.query.filter_by(first_name=first_name, last_name=last_name).first()
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
                    employee.first_name = first_name.title()
                    employee.last_name = last_name.title()

        if employee.email != email:
            email_exists = Employee.query.filter_by(email=email).first()
            if email_exists:
                flash('Email is already in use.', category='error')
                errors = True
            else:
                if  (len(email) < 8) or "@" not in email or "." not in email:
                    flash("Email is invalid.", category='error')
                    errors = True
                else:
                    employee.email = email

        if employee.address != address:
            address_exists = Employee.query.filter_by(address=address).first()
            if address_exists:
                flash('Address is already in use.', category='error')
                errors = True
            else:
                employee.first_name = first_name
        
        if password1 or password2 != "":
            flash("You need to confirm your password before changing", category='error')
            errors = True
        elif password2 != "" and password2 != "" and password1 == password2 and password1 != employee.password:
            employee.password = generate_password_hash(password1, method='sha256')
            flash('Password changed', category='success')
        
        if employee.position != position:
            employee.position = position

        if errors == False:
            employee.date_updated = datetime.now()
            
            db.session.commit()
            flash(employee.date_updated)
            return redirect(url_for('views.employees'))

    return render_template("editEmployee.html", employee=employee, empCols=empCols)

@views.route("/new-employee", methods=['GET', 'POST'])
@login_required
def newEmployee():
    employees = Employee.query.all()
    empCols = GetCols("Employee")

    if empCols.__contains__("id"):
        empCols.remove("id")
    if empCols.__contains__("date_created"):
        empCols.remove("date_created")
    if empCols.__contains__("date_updated"):
        empCols.remove("date_updated")

    if request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        address = request.form.get("address")
        if empCols.__contains__("password"):
            password = request.form.get("password")
        position = str(request.form.get("position"))
        errors = False

        email_exists = Employee.query.filter_by(email=email).first()
        address_exists = Employee.query.filter_by(address=address).first()
        name_exists = Employee.query.filter_by(first_name=first_name, last_name=last_name).first()
        
        if name_exists:
            flash('Name combination is already in use.', category='error')
        elif len(first_name) < 3:
            flash('First name must be at least 3 characters long.', category='error')
        elif len(last_name) < 3:
            flash('Last name must be at least 3 characters long.', category='error')
        elif email_exists:
            flash('Email is already in use.', category='error')
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
        elif address_exists:
            flash('Address is already in use.', category='error')
        else:
            new_employee = Employee(first_name=first_name, last_name=last_name, email=email, address=address, password=generate_password_hash("password", method='sha256'), position=position, date_created=datetime.now(), date_updated=datetime.now())
            db.session.add(new_employee)
            db.session.commit()
            return redirect(url_for('views.employees'))

    return render_template("newEmployee.html", employee=current_user, employees=employees, empCols=empCols)



@views.route("/delete-client/<id>")
@login_required
def deleteClient(id):
    client = Client.query.filter_by(id=id).first()

    conn = sqlite3.connect("files/database.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM client")
    result = cur.fetchone()
    if result[0]-1 == 0:
        flash('Can\'t delete the last client', category='error')
        db.session.rollback()
        db.session.commit()
    else:
        db.session.delete(client)
        db.session.commit()
    
    return redirect(url_for('views.clients'))


@views.route("/delete-employee/<id>")
@login_required
def deleteEmployee(id):
    employee = Employee.query.filter_by(id=id).first()

    conn = sqlite3.connect("files/database.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM employee")
    result = cur.fetchone()
    if result[0]-1 == 0:
        flash('Can\'t delete the last employee', category='error')
        db.session.rollback()
        db.session.commit()
    else:
        if employee != current_user:
            db.session.delete(employee)
            db.session.commit()
        else:
            flash('Cannot delete your own profile while using it', category='error')
    
    return redirect(url_for('views.employees'))
