from flask import (Blueprint, render_template, request, session, url_for, make_response, flash, redirect)
from flask_login import login_required, login_user, current_user, logout_user

from .forms import RegisterForm, LoginForm
from .models import User

from .. import db, bcrypt

bp = Blueprint("user_bp", __name__)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("user_bp.login"))

@bp.route("/login", methods=["GET", "POST"])
def login():
     if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("index_bp.index"))
     form = LoginForm(request.form)
     if form.validate_on_submit():
          user = User.query.filter_by(email=form.email.data).first()
          if user and bcrypt.check_password_hash(user.password, request.form["password"]):
               login_user(user)
               return redirect(url_for("index_bp.index"))
          else:
               flash("Invalid email and/or password.", "danger")
               return render_template("login.html", form=form)
     return render_template("login.html", form=form)

@bp.route("/signup", methods=["GET", "POST"])
def signup():
     if current_user.is_authenticated:
          flash("You are already registered.", "info")
          return redirect(url_for("index_bp.index"))
     form = RegisterForm(request.form)
     if form.validate_on_submit():
          user = User(email=form.email.data, password=form.password.data)
          db.session.add(user)
          db.session.commit()

          login_user(user)
          flash("You registered, nice!", "success")

          return redirect(url_for("user_bp.profile"))
     
     return render_template("signup.html", form=form)

     # if request.method == "POST":
     #      pass
     # else:
     #      return render_template("signup.html")
     
@bp.route("/profile")
@login_required
def profile():
     return "you are logged in!!!!!"