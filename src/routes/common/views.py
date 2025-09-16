from flask import (Blueprint, render_template, request, session, url_for, make_response)

bp = Blueprint("index_bp", __name__)

from .models import count_visit

@bp.route("/")
@count_visit("/")
def index():
    return render_template("index.html")

@bp.route("/about")
def about():
     return render_template("about.html")

@bp.route("/roadmap")
def roadmap():
     return render_template("roadmap.html")

@bp.route("/contribute")
def contribute():
     return render_template("contribute.html")