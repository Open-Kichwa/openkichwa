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
login_manager.init_app(app) 
login_manager.login_view = "user_bp.login"
login_manager.login_message_category = "danger"

babel.init_app(app, locale_selector=get_locale)
@app.context_processor
def inject_get_locale():
    return dict(get_locale=get_locale)

app.config['TEMPLATES_AUTO_RELOAD'] = True

from . import index
app.register_blueprint(index.bp)

from .legal.views import bp as legal_bp
app.register_blueprint(legal_bp)

from .user.views import bp as user_bp
app.register_blueprint(user_bp)

from .user.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()



with app.app_context():

    from .user import models

    if app.config.get("TESTING") or app.config.get("DEBUG") or app.config.get("DEVELOPMENT"):
        db.create_all() 

@app.cli.command("drop-db")
def drop_db():
    """Drop all DB tables."""
    confirm = input("Drop all tables? Type 'yes' to confirm: ")
    if confirm == "yes":
        with app.app_context():
            db.drop_all()
        print("Dropped")
    else:
        print("Aborted")

import click

@app.cli.command("create-beta")
@click.option("--created-for", default=None, help="Optional description of who this code is for")
def create_one_code(created_for):
    from .user.models import AccessCode, AccessCodeTypes
    

    while True:
        if created_for:
            code = AccessCode(
                ctype=AccessCodeTypes.BETA,
                created_for=created_for
            )
        else:
            code = AccessCode(
                ctype=AccessCodeTypes.BETA,
            )
        code_str = code.code
        existing = AccessCode.query.filter_by(code=code_str).first()
        if not existing:
            break

    db.session.add(code)
    db.session.commit()
    click.echo(f"Generated BETA access code: {code.code}")
