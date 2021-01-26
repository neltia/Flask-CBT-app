from main import *
from flask import Blueprint

blueprint = Blueprint("member", __name__, url_prefix='/member')

@blueprint.route("login", methods=["GET", "POST"])
def member_login():
    return render_template("login.html")
