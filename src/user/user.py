from flask import (Blueprint, render_template, request, session, url_for, make_response)

bp = Blueprint("user_bp", __name__)

@bp.route("/login", methods=["GET", "POST"])
def login():
     if request.method == "POST":
          pass
     else:
          return render_template("login.html")


@bp.route("/signup", methods=["GET", "POST"])
def signup():
     if request.method == "POST":
          pass
     else:
          return render_template("signup.html")