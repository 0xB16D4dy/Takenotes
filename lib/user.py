import email
from flask import Blueprint, redirect, render_template, request, flash, session, url_for
from .models import User
import re 
from sqlalchemy.sql.expression import false
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

from flask_login import login_user, login_required, logout_user, current_user
user = Blueprint("user", __name__)

def is_email_address_valid(email):
    """Validate the email address using a regex."""
    if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
        return False
    return True


@user.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
    
        user = User.query.filter_by(email = email).first()
        if user:
            flash("Email existed!", category="error")
        elif not is_email_address_valid(email):
            flash("Please enter a valid email address", category="error")
        elif len(password) < 7:
            flash("Please enter length password > 7 ", category="error")
        elif password != confirm_password:
            flash("Password doesn't match!", category="error")
        else:
            password = generate_password_hash(password, method="sha256")
            new_user = User(email, password, user_name)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("User created!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            except:
                "Create failed!"
    return render_template('register.html', user=current_user)


@user.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                session.permanent = True
                login_user(user, remember=True)
                flash("Logged in Success!",category="success")
                return redirect(url_for('views.home'))
            else:
                flash("Wrong password, please try again!", category="error")
        else:
            flash("User doesn't exist!", category="error")
    return render_template('login.html', user=current_user)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.logout"))
