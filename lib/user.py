from .models import User, Note
from . import db, mail, app
from .forms import *
from PIL import Image
from flask import Blueprint, redirect, render_template, request, flash, session, url_for, current_app
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
# from flask_wtf import FlaskForm
import secrets
import os
import base64
import sys

user = Blueprint("user", __name__)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = app.root_path+"\\static\\assets\\img\\profile_pics\\"+picture_fn
    # picture_path = os.path.join(current_app.root_path, "/static/assets/img/profile_pics/", form_picture.filename)
    #form_picture.save(picture_path)
    output_size = (125 , 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg =  Message("Password Reset Request", 
                    sendejr="hlhphuoc170821@gmail.com", 
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
                return redirect(url_for("views.home"))
                # return "User Created"
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


    
@user.route('/account', methods=["GET","POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file 
        current_user.user_name = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been update', category="success")
        return redirect(url_for("user.account"))
    elif request.method == "GET":
        form.username.data = current_user.user_name
        form.email.data = current_user.email
    image_file = url_for('static', filename='assets/img/profile_pics/' + current_user.image_file)
    return render_template("account.html", title = "Account", user = current_user, image_file=image_file, form=form)


@user.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = Note.query.filter(Note.data.like('%' + form.search.data + '%'))
        #print(results)
        return render_template('search.html', user = current_user, form=form, results=results)
    return render_template('search.html', user = current_user, form=form)

@user.route('/uploadFile', methods=["GET","POST"])
def upload_file():
    form = UploadFile()
    if request.method == 'POST':
        f = request.files['file']
        file_string = base64.b64encode(f.read())
        file_string = base64.b64decode(file_string)
        file_string = file_string.decode('utf-8')
        if len(file_string) < 1:
            flash('Note is too short!', category="danger")
        else:
            new_note = Note(data = file_string, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category="success")
        return redirect(url_for("views.home"))