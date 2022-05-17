from flask import Blueprint, render_template
from flask_login import current_user, login_required
# from sqlalchemy.sql.functions import user

views = Blueprint("views", __name__)

@views.route('/home')
@views.route('/')
# @login_required
def home():
    return render_template('index.html', user=current_user)