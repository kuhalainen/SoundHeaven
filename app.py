import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import tracks
import users
import tags
import comments
import files


app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    recent_tracks = tracks.get_items(10)
    return render_template("index.html", items=recent_tracks)


@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_tracks = users.get_items(user_id)
    return render_template("show_user.html",user=user, user_tracks=user_tracks)


@app.route("/track/<int:track_id>")
def show_track(track_id):
    track = tracks.get_item(track_id)
    if not track:
        abort(404)
    track_tags = tags.track_tags(track_id)
    track_comments = comments.get_track_comments(track_id)
    track_image = files.get_album_art(track_id)[0]

    return render_template("show_track.html",track=track, track_tags=track_tags, track_comments=track_comments, track_image=track_image)

@app.route("/search")
def search():
    query = request.args.get("query")
    if query:
        result = tracks.find_items(query)
    else:
        query = ""
        result = []
    return render_template("search.html", query=query, result=result)                                        

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create_account", methods=["POST"])
def create_account():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    try:
        users.create_user(username, password1)

    except:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username,password)

        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    require_login()
    if "user_id" in session:
        del session["username"]
        del session["user_id"]
    return redirect("/")

@app.route("/new_track")
def new_track():
    require_login()
    return render_template("new_track.html")

@app.route("/create_track", methods=["POST"])
def create_track():
    require_login()

    title = request.form["title"]
    if len(title) > 50 or not title:
        abort(403)
    desc = request.form["desc"]
    if len(desc) > 1000:
        abort(403)
    track_tags = request.form["tags"]
    if len(track_tags) > 150:
        abort(403)
    taglist = tags.parse_tags(track_tags)
    if not taglist:
        abort(403)

    file = request.files["image"]
    valid = files.check_image(file)

    if valid[0] != True:
        return valid

    files.save_image(valid[1], valid[2])
    image_id = db.last_insert_id()

    user_id = session["user_id"]

    tracks.add_item(title,desc,user_id)
    track_id = db.last_insert_id()
    tags.create_tags(taglist)
    tags.assign_tags(track_id, taglist)
    print(track_id)
    print(image_id)
    files.set_album_art(track_id, image_id)

    return redirect("/")

@app.route("/edit_track/<int:track_id>")
def edit_track(track_id):
    require_login()
    track = tracks.get_item(track_id)
    if not track:
        abort(404)
    if session["user_id"] != track["user_id"]:
        abort(403)
    track_tags = tags.track_tags(track_id)
    return render_template("edit_track.html", track=track, track_tags=track_tags)

@app.route("/update_track", methods=["POST"])
def update_track():
    require_login()
    track_id = request.form["track_id"]

    track = tracks.get_item(track_id)
    if not track:
        abort(404)
    if session["user_id"] != track["user_id"]:
        abort(403)

    title = request.form["title"]
    if len(title) > 50 or not title:
        abort(403)
    desc = request.form["desc"]
    if len(desc) > 1000:
        abort(403)
    track_tags = request.form["tags"]
    if len(track_tags) > 150:
        abort(403)
    taglist = tags.parse_tags(track_tags)
    if not taglist:
        abort(403)


    tracks.update_item(title,desc,track_id)

    tags.remove_track_tags(track_id)
    tags.create_tags(taglist)
    tags.assign_tags(track_id, taglist)



    return redirect("/track/" + str(track_id))

@app.route("/remove_track/<int:track_id>", methods=["GET", "POST"])
def remove_track(track_id):
    require_login()
    track = tracks.get_item(track_id)
    if not track:
        abort(404)
    if session["user_id"] != track["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("remove_track.html", track=track)

    if request.method == "POST":
        if "remove" in request.form:
            tags.remove_track_tags(track_id)
            tracks.remove_item(track_id)

            return redirect("/")
        else:
            return redirect("/track/" + str(track_id))

@app.route("/track/<int:track_id>/create_comment", methods=["POST"])
def create_comment(track_id):
    require_login()
    track = tracks.get_item(track_id)
    if not track:
        abort(403)
    comment = request.form["comment"]
    if not comment or len(comment) > 150:
        abort(403)

    comments.create_comment(track_id, session["user_id"], comment)
    return redirect("/track/" + str(track_id))


@app.route("/remove_comment/<int:comment_id>", methods=["POST"])
def remove_comment(comment_id):
    require_login()

    track_id = request.form["track_id"]
    comment = comments.get_comment(comment_id)
    if not comment:
        abort(403)
    if session["user_id"] != comment["user_id"]:
        abort(403)

    comments.delete_comment(comment["id"])
    return redirect("/track/" + str(track_id))

@app.route("/add_image", methods=["GET", "POST"])
def add_image():
    require_login()

@app.route("/image/<int:image_id>")
def show_image(image_id):
    image = files.get_image(image_id)
    if not image:
        abort(404)

    response = make_response(bytes(image[0][1]))
    response.headers.set("Content-Type", "image/jpeg")
    return response
