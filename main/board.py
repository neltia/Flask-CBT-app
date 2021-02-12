from main import *
from flask import Blueprint
from flask import send_file
from flask import send_from_directory

blueprint = Blueprint("board", __name__, url_prefix='/board')

@blueprint.route("/")
@blueprint.route("/list")
def board_main():
    return render_template("board.html")


@blueprint.route("/view/<idx>")
def board_view():
    if idx is not None:
        board = mongo.db.board
        data = board.find_one({"_id": ObjectId(idx)})
        if data is not None:
            result = {
                "id": data.get("_id"),
                "name": data.get("name"),
                "title": data.get("title"),
                "contents": data.get("contents"),
                "date": data.get("date"),
                "writer_id": data.get("writer_id", ""),
                "attachfile": data.get("attachfile", "")
            }
            comment = mongo.db.comment
            comments = comment.find({"root_idx": str(data.get("_id"))})
            return render_template("view.html", result=result, comments=comments)
    return abort(404)


@blueprint.route("/write")
def board_write():
    form = writeForm()
    if request.method == "POST":
        filename = None
        if "attachfile" in request.files:
            file = request.files["attachfile"]
            if file and allowed_file(file.filename, "file"):
                filename = check_filename(file.filename)
                file.save("./static/files/" + filename)

        writer_id = session.get("email")
        title = request.values.get("title")
        contents = request.values.get("content")

        board = mongo.db.board
        tot_count = board.count_documents({})
        cur_utc_time = round(datetime.utcnow().timestamp() * 1000)
        post = {
            "writer_id": writer_id,
            "num": tot_count + 1,
            "title": title,
            "contents": contents,
            "date": cur_utc_time,
        }

        if filename is not None:
            post["attachfile"] = filename
        x = board.insert_one(post)
        return redirect(url_for("board.board_view", idx=x.inserted_id))
    else:
        return render_template("write.html", form=form, name=session["email"].split("@")[0])


@blueprint.route("/edit/<idx>", methods=["GET", "POST"])
def board_edit(idx):
    form = writeForm()
    if request.method == "GET":
        board = mongo.db.board
        data = board.find_one({"_id": ObjectId(idx)})
        if data is None:
            flash("해당 게시물이 존재하지 않습니다.")
            return redirect(url_for("main_page"))
        else:
            if session.get("id") == data.get("writer_id"):
                return render_template("edit.html", form=form, data=data)
            else:
                flash("글 수정 권한이 없습니다.")
                return redirect(url_for("main_page"))
    else:
        title = request.form.get("title")
        contents = request.form.get("contents")
        board = mongo.db.board

        data = board.find_one({"_id": ObjectId(idx)})

        if data.get("writer_id") == session.get("id"):
            board.update_one({"_id": ObjectId(idx)}, {
                "$set": {
                    "title": title,
                    "contents": contents,
                }
            })
            flash("수정되었습니다.")
            return redirect(url_for("board_view", idx=idx))
        else:
            flash("글 수정 권한이 없습니다.")
            return redirect(url_for("main_page"))


@blueprint.route("/delete/<idx>")
def board_delete(idx):
    board = mongo.db.board
    data = board.find_one({"_id": ObjectId(idx)})
    if data.get("writer_id") == session.get("id"):
        board.delete_one({"_id": ObjectId(idx)})
        flash("삭제되었습니다.")
    else:
        flash("글 삭제 권한이 없습니다.")
    return redirect(url_for("main_page"))


@blueprint.route("/upload_image", methods=["POST"])
def upload_image():
    if request.method == "POST":
        img_file = request.files["image"]
        print(img_file)
        if img_file and allowed_file(img_file.filename, "img"):
            filename = "{}_{}.jpg".format(str(int(datetime.now().timestamp()) * 1000), rand_generator())
            print(filename)
            savefilepath = os.path.join("./static/images", filename)
            print(savefilepath)
            img_file.save(savefilepath)
            return url_for("board_images", filename=filename)


@blueprint.route('/images/<filename>')
def board_images(filename):
    return send_from_directory('./static/images', filename)


@blueprint.route('/files/<filename>')
def board_files(filename):
    return send_file('./static/files/' + filename,
                    attachment_filename = filename,
                    as_attachment=True)


@blueprint.route("/comment_write", methods=["POST"])
def comment_write():
    try:
        print(session["id"])
    except:
        flash("회원가입 후 댓글을 달 수 있습니다.")
        return redirect(url_for("member_login"))

    if request.method == "POST":
        name = session.get("name")
        writer_id = session.get("id")
        root_idx = request.form.get("root_idx")
        ccomment = request.form.get("comment")
        current_utc_time = round(datetime.utcnow().timestamp() * 1000)

        comment = mongo.db.comment

        post = {
            "root_idx": root_idx,
            "writer_id": writer_id,
            "name": name,
            "comment": ccomment,
            "date": current_utc_time,
        }

        print(post)
        comment.insert_one(post)
        return redirect(url_for("board_view", idx=root_idx))
    return abort(404)


@blueprint.route("/comment_delete/<idx>")
def comment_delete(idx):
    comment = mongo.db.comment
    data = comment.find_one({"_id": ObjectId(idx)})
    if data.get("writer_id") == session.get("id"):
        comment.delete_one({"_id": ObjectId(idx)})
        flash("삭제되었습니다.")
    else:
        flash("댓글 삭제 권한이 없습니다.")
    return """<script>
        window.location = document.referrer;
        </script>"""


