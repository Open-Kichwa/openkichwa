from flask_babel import Babel
from flask import request

def get_locale():
    if "lang" in request.args:
        language = request.args["lang"]
    else:
        language = request.accept_languages.best_match(["en", "es"])
    
    return language

babel = Babel()
