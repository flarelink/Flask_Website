import os


class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')  # secret key to protect against attacks; stored in your .bashrc
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')  # database
    MAIL_SERVER = 'smtp.googlemail.com'  # setting up mail server
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('DB_USER')  # stored in .bashrc
    MAIL_PASSWORD = os.environ.get('DB_PASS')  # stored in .bashrc
    SQLALCHEMY_TRACK_MODIFICATIONS = False
