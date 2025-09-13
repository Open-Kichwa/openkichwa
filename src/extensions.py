from flask_babel import Babel
from flask import request, session

def get_locale():
    if 'lang' in request.args:
        session['lang'] = request.args.get('lang')
    
    if 'lang' in session:
        return session['lang']
    
    return request.accept_languages.best_match(['en', 'es'])

babel = Babel()
