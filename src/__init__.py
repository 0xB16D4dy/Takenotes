import os
from datetime import timedelta
from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from flask_mail import Mail


db = SQLAlchemy()
mail = Mail()
app = Flask(__name__)

load_dotenv()
SECRET_KEY = os.environ.get("KEY")
DB_NAME = os.environ.get("DB")
EMAIL = os.environ.get("EMAIL_USER")
PASS = os.environ.get("EMAIL_PASS")

def create_database(app):
    if not os.path.exists("lib/"+ DB_NAME):
        db.create_all(app=app)
        print("Create DB!")

def create_app():
    
    #config database
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    Bootstrap(app)
    db.__init__(app)
    
   
    # from .models import Upload
    from .models import User
    create_database(app)


    from src.user import user
    # . goị từ thằng cha
    from .views import views
    app.register_blueprint(user)
    app.register_blueprint(views)

    login_manager = LoginManager(app)
    login_manager.init_app(app)
    login_manager.login_view = "user.login"
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
   
     #config mailserver 
    app.config["MAIL_SERVER"] = "smtp.googlemail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = EMAIL           
    app.config["MAIL_PASSWORD"] = PASS
    mail.__init__(app)

    
    

    # set the time of a session in 5 minutes
    app.permanent_session_lifetime = timedelta(minutes=5)

    return app
