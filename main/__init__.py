from flask import Flask # flask packages
from flask import request
from flask import render_template
from flask import redirect, url_for
from flask import session
from flask import flash
from flask_pymongo import PyMongo # Database
from bson.objectid import ObjectId
from datetime import datetime # Others
import hashlib
import os


app = Flask(__name__) 
app.config["MONGO_URI"] = "mongodb://localhost:27017/cbtTalk"
mongo = PyMongo(app)
salt = 'neltia' # secret key
now = str(datetime.now())
myHash = hashlib.sha512(str(now + salt).encode('utf-8')).hexdigest()
app.config['SECRET_KEY'] = myHash


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not.html"), 404


@app.route("/")
def index():
    return redirect(url_for("page.page_cover"))


from . import page
from . import member
from . import board


app.register_blueprint(page.blueprint)
app.register_blueprint(member.blueprint)
app.register_blueprint(board.blueprint)
