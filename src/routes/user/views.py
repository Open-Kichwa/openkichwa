from flask import (Blueprint, render_template, request, session, url_for, make_response, flash, redirect)
from flask_login import login_required, login_user, current_user, logout_user
from flask_babel import gettext
from datetime import datetime

from .forms import RegisterForm, LoginForm
from .models import User, AccessCode

from ... import db, bcrypt, babel
from ...routes.common.models import count_visit

bp = Blueprint("user_bp", __name__)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("user_bp.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():
     if request.method == "POST":
          if current_user.is_authenticated:
               flash(gettext("You are already logged in"), "info")
               return redirect(url_for("index_bp.index"))
          
          form = LoginForm(request.form)
          if form.validate_on_submit():
               user = User.query.filter_by(email=form.email.data).first()
               if user and bcrypt.check_password_hash(user.password, request.form["password"]):
                    login_user(user)
                    return redirect(url_for("index_bp.index"))
               else:
                    flash(gettext("Invalid email and/or password"), "danger")
                    return render_template("user/login.html", form=form)
          return render_template("user/login.html", form=form)
     else:
          form = LoginForm()
          return render_template("user/login.html", form=form)

@count_visit("/signup")
@bp.route("/signup", methods=["GET", "POST"])
def signup():
     if request.method == "POST":
          if current_user.is_authenticated:
               flash(gettext("You are already registered"), "info")
               return redirect(url_for("index_bp.index"))
          form = RegisterForm(request.form)
          if form.validate_on_submit():
               user = User(email=form.email.data, password=form.password.data, community=form.community.data, name=form.username.data)
               db.session.add(user)
               db.session.flush()

               code: AccessCode = AccessCode.query.filter_by(code=form.beta_code.data).first()
               user.access_code_id = code.id
               code.claimed = True
               code.claimed_on = datetime.now()
               code.user_id = user.id        
               db.session.commit()

               login_user(user)
               flash(gettext("You have been registered!"), "success")

               return redirect(url_for("user_bp.profile"))
          return render_template("user/signup.html", form=form)
     else:     
          form = RegisterForm()
          return render_template("user/signup.html", form=form)

     
@bp.route("/profile")
@login_required
def profile():
     return "you are logged in!!!!!"