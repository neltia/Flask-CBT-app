from flask import Flask # flask packages
from flask import request
from flask import render_template
from flask import redirect, url_for
from flask import session, abort
from flask import flash
from flask_pymongo import PyMongo # Database
from bson.objectid import ObjectId
from datetime import datetime # Others
import hashlib
import os

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms.widgets import TextArea
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email

app = Flask(__name__) 
app.config["MONGO_URI"] = "mongodb://localhost:27017/cbtTalk"
mongo = PyMongo(app)
salt = 'neltia' # secret key
now = str(datetime.now())
myHash = hashlib.sha512(str(now + salt).encode('utf-8')).hexdigest()
app.config['SECRET_KEY'] = myHash


class writeForm(FlaskForm):
    title = StringField("제목", validators=[DataRequired()])
    content = StringField("내용", widget=TextArea())


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not.html"), 404


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None or session.get("id") == "":
            return redirect(url_for("member_login", next_url=request.url))
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename, types):
    if types == "img":
        return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS_img
    if types == "file":
        return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS_file


def check_filename(filename):
    reg = re.compile(r'[^A-Za-z0-9_.가-힝-]')
    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, ' ')
            print(filename)
            filename = str(reg.sub('', '_'.join(filename.split()))).strip('._')
    return filename


def rand_generator(length=8):
    chars = ascii_lowercase + ascii_uppercase + digits
    return ''.join(random.sample(chars, length))


@app.route("/")
def index():
    return redirect(url_for("page.page_cover"))


from . import page
from . import member
from . import board


app.register_blueprint(page.blueprint)
app.register_blueprint(member.blueprint)
app.register_blueprint(board.blueprint)
