from flask import (Blueprint, render_template, request, session, url_for, make_response)

bp = Blueprint("index", __name__)

@bp.route("/")
def index():
    return render_template("index.html")