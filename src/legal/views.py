from flask import (Blueprint, render_template, request, session, url_for, make_response, send_from_directory, Response)

bp = Blueprint("legal_bp", __name__)

@bp.route("/terms")
def terms():
     return render_template("legal/terms.html")

@bp.route("/robots.txt")
def robots():
     robots =  """
     # robots.txt file for Open Kichwa / Kichwa Paskana
     # Created with love from Germany <3
     
     User-agent: *
     Disallow: /profile
     Disallow: /terms
     Disallow: /signup
     Disallow: /login
     Disallow: /logout
"""  
     return Response(robots, mimetype="text/plain")


# TODO:
# Privacy, cookie banner, imprint