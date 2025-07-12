from flask import Flask

from .extensions import babel, get_locale

def create_app(test_config=None):
    app = Flask(__name__)
    babel.init_app(app, locale_selector=get_locale)

    app.config['TEMPLATES_AUTO_RELOAD'] = True

    from . import index
    app.register_blueprint(index.bp)


    return app