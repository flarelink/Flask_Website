import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')  # secret key to protect against attacks; stored in your .bashrc if you forget
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # database; /// means relative path so will be local
db = SQLAlchemy(app)  # make SQLAlchemy database instance
bcrypt = Bcrypt(app)  # encryption for passwords so that they aren't stored in plaintext
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'  # setting up mail server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('DB_USER')  # stored in .bashrc
app.config['MAIL_PASSWORD'] = os.environ.get('DB_PASS')  # stored in .bashrc
mail = Mail(app)

from flask_site import routes
