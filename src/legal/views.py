from flask import (Blueprint, render_template, request, session, url_for, make_response)

bp = Blueprint("legal_bp", __name__)

@bp.route("/terms")
def terms():
     return render_template("legal/terms.html")