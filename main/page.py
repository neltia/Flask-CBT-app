from main import *
from flask import Blueprint

blueprint = Blueprint("page", __name__, url_prefix='/page')

@blueprint.route("/cover")
def page_cover():
    return render_template("cover.html")


@blueprint.route("/main")
def page_main():
    return render_template("index.html")
