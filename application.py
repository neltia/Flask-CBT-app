""" Call Lib """
# flask main lib
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect, url_for

# flask plus lib
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.fields.html5 import IntegerField
from wtforms import validators
from datetime import datetime
import hashlib
import bcrypt
from flask_mail import Mail, Message

# else lib
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# firebase
# import fdb_api
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.Certificate('./static/private/dbkey.json')
firebase_admin.initialize_app(cred, {
  'projectId': 'neltia-manage',
})

db = firestore.client()

# secret_key
salt = 'neltia'
now = str(datetime.now())
myHash = hashlib.sha512(str(now + salt).encode('utf-8')).hexdigest()

app = Flask(__name__)
app.config['SECRET_KEY'] = myHash
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'jhsm9534@gmail.com'
f = open("password.txt",'r')
app.config['MAIL_PASSWORD'] = f.read()
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Form Field
class ContactForm(FlaskForm):
    name = StringField("사용자 이름",  [validators.DataRequired()])
    email = EmailField('이메일 주소', [validators.DataRequired(), validators.Email()])
    pw = PasswordField("비밀번호",  [validators.DataRequired()])
    code = StringField('인증코드', [validators.DataRequired()])

#Error Process
@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not.html'), 404

# enter page
@app.route("/")
def cover_page():
    return render_template("cover.html")

# main page
@app.route("/index")
def index_page():
    #url_itNews = requests.get("http://www.itnews.or.kr/?cat=1162", verify=False)
    #url_boanNews = requests.get("https://www.boannews.com/media/t_list.asp", verify=False)
    news = "이거 엄청 중요한 소식이야"
    return render_template("index.html", news=news)

# board page
@app.route("/note")
def note_page():
    return render_template("note.html")

# board page
@app.route("/board")
def board_page():
    if(request.method == 'GET'):
        return render_template("board.html")    
    else:
        name = request.form['username']
        return render_template("board.html")

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if(request.method == 'GET'):
        form = ContactForm()
        return render_template("login.html", form=form)
    else:
        name = request.form['username']
        passw = request.form['password']
        try:
            data = User.query.filter_by(username=name, password=passw).first()
            if data is not None:
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return 'Dont Login'
        except:
            return "Dont Login"

@app.route("/register")
def signup_page():
    if(request.method == 'GET'):
        form = ContactForm()
        return render_template("register.html", form = form)
    else:
        name = request.form['username']
        passw = request.form['password']
        
        

        

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('/index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
