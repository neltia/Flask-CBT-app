from main import *
from flask import Blueprint

blueprint = Blueprint("board", __name__, url_prefix='/board')

@blueprint.route("/")
@blueprint.route("/list")
def board_main():
    return render_template("board.html")


@blueprint.route("/view/<idx>")
def board_view():
    return "view"


@blueprint.route("/write")
def board_write():
    return "write"
