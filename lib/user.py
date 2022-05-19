from flask import Blueprint, redirect, render_template, request, flash, session, url_for
from .models import User
from . import db, mail
from .forms import *
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
# from flask_wtf import FlaskForm
user = Blueprint("user", __name__)


def send_reset_email(user):
    token = user.get_reset_token()
    # from . import mail
    msg =  Message("Password Reset Request", 
                    sender="hlhphuoc170821@gmail.com", 
                    recipients = [user.email])
    msg.body =  f''' To reset your password, visit the following link:
{url_for("user.reset_token", token = token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@user.route('/signup', methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return  redirect(url_for("views.home"))
    form = registerForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            flash("Email existed!", category="danger")
        elif not is_email_address_valid(form.email.data):
            flash("Please enter a valid email address", category="danger")
        elif len(form.password.data) < 7:
            flash("Please enter length password > 7 ", category="danger")
        elif form.password.data != form.confirm_password.data:
            flash("Password doesn't match!", category="danger")
        else:
            email = form.email.data
            password = generate_password_hash(form.password.data, method="sha256")
            user_name = form.username.data

            new_user = User(email, password, user_name)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash(f"User {form.username.data} created!", category="success")
                login_user(user, remember=True)
                # return redirect(url_for("views.home"))
                return "User Created"
            except:
                "Create failed!"

    return render_template("signup.html", form = form , user= current_user)

@user.route('/sigin', methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return  redirect(url_for("views.home"))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name = form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                session.permanent = True
                login_user(user, remember = form.remember.data)
                # Sửa để không hiện ra next=%2F<account> trên url nữa
                next_page = request.args.get("netxt")
                return redirect(next_page) if next_page else redirect(url_for("views.home"))
                # flash("Logged in Success!",category="success")
                # return redirect(url_for('views.home'))
            else:
                flash("Wrong password, please try again!", category="danger")    

    return render_template("signin.html", form = form , user= current_user)


@user.route('/reset_password', methods=["GET","POST"])
def reset_request():
    if current_user.is_authenticated:
        return  redirect(url_for("views.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.", category = "info")
        return redirect(url_for("user.login"))
    return render_template("reset_request.html", tittle = "Reset Password", form = form, user = current_user)

@user.route('/reset_password/<token>', methods=["GET","POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return  redirect(url_for("views.home"))
    user = User.verify_reset(token)
    if user is None:
        flash("That is an invalid or expired token", category = "warning")
        return redirect(url_for("user.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        new_password = generate_password_hash(form.password.data, method="sha256")
        user.password = new_password
        db.session.commit()
        flash("Your password has been update! You are now able to log in", category="success")
        return redirect(url_for("user.signin"))
    return render_template("reset_with_token.html", tittle = "Reset Password", form = form, user = current_user)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))


@user.route('/account')
@login_required
def account():
    form = UpdateAccountForm()
    image_file = url_for('static', filename='assets/img/profile_pics/' + current_user.image_file)
    return render_template("account.html", title = "Account", user = current_user, image_file=image_file, form=form)