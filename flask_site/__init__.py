from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_site.config import Config


db = SQLAlchemy()  # make SQLAlchemy database instance
bcrypt = Bcrypt()  # encryption for passwords so that they aren't stored in plaintext
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # import all routing for site
    from flask_site.users.routes import users
    from flask_site.posts.routes import posts
    from flask_site.main.routes import main
    from flask_site.errors.handlers import errors

    # register the blueprints for the full application
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
