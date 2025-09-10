from flask import Flask
from decouple import config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from .extensions import babel, get_locale

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app) # Continue from user_loader
babel.init_app(app, locale_selector=get_locale)

app.config['TEMPLATES_AUTO_RELOAD'] = True

from . import index
app.register_blueprint(index.bp)

from .user import user
app.register_blueprint(user.bp)
