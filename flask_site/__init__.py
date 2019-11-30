from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '6db96e6441e9bc1ebf126dccb395aed0'  # secret key to protect against attacks
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # database; /// means relative path so will be local
db = SQLAlchemy(app)  # make SQLAlchemy database instance

from flask_site import routes