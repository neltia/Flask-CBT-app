from main import *
from flask import Blueprint

blueprint = Blueprint("member", __name__, url_prefix='/member')

@blueprint.route("login", methods=["GET", "POST"])
def member_login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pass")

        members = mongo.db.members
        data = members.find_one({"email": email})
        
        if data is None:
            msg = "회원정보가 없습니다."
            return render_template("register.html", msg=msg)
        else:
            if data.get("pass") == hashlib.sha512(password.encode()).hexdigest():
                session["email"] = email
                session['logged_in'] = True
                return redirect(url_for("page.page_main"))
            else:
                msg = "아이디나 비밀번호가 올바르지 않습니다."
                return render_template("login.html", msg=msg)
    else:
        abort(404)


@blueprint.route("register", methods=["GET", "POST"])
def member_new():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        email = request.form.get("email", type=str)
        pass1 = request.form.get("pass1", type=str)
        pass2 = request.form.get("pass2", type=str)
        
        if email is None or pass1 is None or pass2 is None:
            msg = "입력되지 않은 값이 있습니다."
            return render_template("register.html", msg=msg)

        members = mongo.db.members
        data = members.find_one({"email": email})
        if data is not None:
            msg = "이미 있는 이메일입니다."
            return render_template("register.html", msg=msg)

        if(len(pass1) < 8):
            msg = "비밀번호는 8자리 이상으로 작성해주세요."
            return render_template("register.html", msg=msg)

        if pass1 != pass2:
            flash("비밀번호가 일치하지 않습니다.")
            return render_template("register.html")
        
        cur_utc_time = round(datetime.utcnow().timestamp() * 1000)
        members = mongo.db.members
        post = {
            "email": email,
            "pass": hashlib.sha512(pass1.encode()).hexdigest(),
            "registerdate": cur_utc_time
        }
        members.insert_one(post)
        flash("가입이 완료되었습니다!")
        return redirect(url_for("member.member_login"))
    else:
        abort(404)


@blueprint.route("logout")
def member_logout():
    del session["email"]
    session["logged_in"] = False
    return """<script>
        window.location = document.referrer;
        </script>"""
