from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '6db96e6441e9bc1ebf126dccb395aed0'  # secret key to protect against attacks
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # database; /// means relative path so will be local
db = SQLAlchemy(app)  # make SQLAlchemy database instance
bcrypt = Bcrypt(app)  # encryption for passwords so that they aren't stored in plaintext
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flask_site import routes