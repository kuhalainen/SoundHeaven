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
import datetime


app = Flask(__name__)
app.secret_key = config.secret_key

appHasRunBefore = False

#Clear session before each server startup
#
#Before adding this, logins could transfer from
#other flask applications written for the TIKAWE course that
#also run as localhost with the same address and port

@app.before_request
def firstRun():
    global appHasRunBefore
    if not appHasRunBefore:
        session.clear()
        appHasRunBefore = True

def require_login():
    if "user_id" not in session:
        abort(403)

def require_logout():
    if "user_id" in session:
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
    if user[2]:
        dt = datetime.datetime.fromtimestamp(user[2] / 1000.0, tz=datetime.timezone.utc)
        dt=dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        dt = None
    return render_template("show_user.html",user=user, user_tracks=user_tracks, dt=dt)


@app.route("/track/<int:track_id>")
def show_track(track_id):
    track = tracks.get_item(track_id)
    if not track:
        abort(404)
    track_tags = tags.track_tags(track_id)
    track_comments = comments.get_track_comments(track_id)
    track_image = files.get_album_art(track_id)
    if track_image:
        track_image = track_image[0]

    track_audio = files.get_track_audio(track_id)
    if track_audio:
        track_audio = track_audio[0]

    return render_template("show_track.html",track=track, track_tags=track_tags, track_comments=track_comments, track_image=track_image, track_audio=track_audio)

@app.route("/search")
def search():
    query = request.args.get("query")
    if query:
        result = tracks.find_items(query)
    else:
        return redirect("/")
        #query = ""
        #result = []
    return render_template("search.html", query=query, result=result)                                        

@app.route("/register")
def register():
    require_logout()
    return render_template("register.html")

@app.route("/create_account", methods=["POST"])
def create_account():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "ERROR: passwords do not match"

    try:
        users.create_user(username, password1)

    except:
        return "ERROR: The username is already in use"

    return redirect("/login")

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
            return "ERROR: wrong username or password"

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
        print("1")
        abort(403)
    desc = request.form["desc"].replace("\r\n", "\n")
    if len(desc) > 1000:
        print(len(desc))
        print(repr(desc))
        print("2")
        abort(403)
    track_tags = request.form["tags"]
    if len(track_tags) > 150:
        print("3")
        abort(403)
    taglist = tags.parse_tags(track_tags)
    if not taglist:
        print("4")
        abort(403)

    image = request.files["image"]
    valid_image = files.check_image(image)

    if valid_image[0] != True:
        return valid_image

    files.save_image(valid_image[1], valid_image[2])
    image_id = db.last_insert_id()

    audio = request.files["audio"]

    valid_audio = files.check_audio(audio)

    if valid_audio[0] != True:
        return valid_audio

    files.save_audio(valid_audio[1], valid_audio[2])
    audio_id = db.last_insert_id()

    user_id = session["user_id"]

    tracks.add_item(title,desc,user_id)
    track_id = db.last_insert_id()
    tags.create_tags(taglist)
    tags.assign_tags(track_id, taglist)
    print(track_id)
    print(image_id)
    files.set_album_art(track_id, image_id)
    files.set_track_audio(track_id, audio_id)

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

    track_image = files.get_album_art(track_id)
    print(track_image)
    if track_image:
        track_image = track_image[0]
        print(track_image[0])

    track_audio = files.get_track_audio(track_id)
    if track_audio:
        track_audio = track_audio[0]

    return render_template("edit_track.html", track=track, track_tags=track_tags, track_image=track_image, track_audio=track_audio)

@app.route("/update_track", methods=["POST"])
def update_track():
    require_login()
    image_id = None
    audio_id = None
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
    
    image = request.files["image"]
    if image:
        valid_image = files.check_image(image)

        if valid_image[0] != True:
            return valid_image

        files.save_image(valid_image[1], valid_image[2])
        image_id = db.last_insert_id()
        
    audio = request.files["audio"]
    if audio:
        valid_audio = files.check_audio(audio)

        if valid_audio[0] != True:
            return valid_audio

        files.save_audio(valid_audio[1], valid_audio[2])
        audio_id = db.last_insert_id()

    tracks.update_item(title,desc,track_id)

    tags.remove_track_tags(track_id)
    tags.create_tags(taglist)
    tags.assign_tags(track_id, taglist)

    if image_id:
        files.remove_album_art(track_id)
        files.set_album_art(track_id, image_id)

    if audio_id:
        files.remove_track_audio(track_id)
        files.set_track_audio(track_id, audio_id)

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
            comments.delete_track_comments(track_id)
            files.remove_album_art(track_id)
            files.remove_track_audio(track_id)
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
    #
    # IMAGE RESIZING NEEDED
    #
    if image[0][2] == "jpg":
        response = make_response(bytes(image[0][1]))
        response.headers.set("Content-Type", "image/jpeg")
        return response
    elif image[0][2] == "png":
        response = make_response(bytes(image[0][1]))
        response.headers.set("Content-Type", "image/png")
        return response
    
@app.route("/audio/<int:audio_id>")
def show_audio(audio_id):
    audio = files.get_audio(audio_id)
    if not audio:
        abort(404)

    if audio[0][2] == "mp3":
        response = make_response(bytes(audio[0][1]))
        response.headers.set("Content-Type", "audio/mpeg")
        return response