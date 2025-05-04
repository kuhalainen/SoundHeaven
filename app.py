import re
import datetime
from flask import Flask
from flask import redirect, render_template, request, session, abort, make_response, flash, g
import db
import config
import tracks
import users
import tags
import comments
import files
import markupsafe
import secrets
import math
import time

app = Flask(__name__)
app.secret_key = config.secret_key

app_has_run_before = False

#Clear session before each server startup
#
#Before adding this, logins could transfer from
#other flask applications written for the TIKAWE course that
#also run as localhost with the same address and port




@app.before_request
def first_run():
    global app_has_run_before
    if not app_has_run_before:
        session.clear()
        app_has_run_before = True

@app.before_request
def before_request():
    g.start_time = time.time()


@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response



def require_login():
    if "user_id" not in session:
        abort(403)

def require_logout():
    if "user_id" in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)


@app.route("/")
def index():
    recent_tracks = tracks.get_items(10)
    return render_template("index.html", items=recent_tracks)

@app.route("/user/<int:user_id>/<int:page>")
@app.route("/user/<int:user_id>")
def show_user(user_id, page=1):
    user = users.get_user(user_id)
    if not user:
        abort(404)

    page_size = 10
    amount = users.find_tracks_amount(user_id)
    #print(amount[0][0])
    page_count = math.ceil(amount[0][0] / page_size)
    page_count = max(page_count, 1)
    #print(page_count)
    user_tracks = users.get_items_paged(user_id, page, page_size)

    if page < 1:
        return redirect("/user/" + str(user_id) + "/1")
    if page > page_count:
        return redirect("/user/" + str(user_id) + "/" + str(page_count))

    if user[2]:
        dt = datetime.datetime.fromtimestamp(user[2] / 1000.0, tz=datetime.timezone.utc)
        dt=dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        dt = None
    #print(user_tracks)
    return render_template("show_user.html",user=user, user_tracks=user_tracks, dt=dt, amount=amount, page=page, page_count=page_count)


@app.route("/track/<int:track_id>/<int:page>")
@app.route("/track/<int:track_id>")
def show_track(track_id, page=1):
    track = tracks.get_item(track_id)
    user = users.get_user(track[3])
    if not track:
        abort(404)
    track_tags = tags.track_tags(track_id)

    page_size = 10
    amount = comments.get_track_comments_amount(track_id)
    #print(amount[0][0])
    page_count = math.ceil(amount[0][0] / page_size)
    page_count = max(page_count, 1)
    #print(page_count)
    track_comments = comments.get_track_comments_paged(track_id, page, page_size)
    
    if page < 1:
        return redirect("/track/"+ str(track_id) + "/1")
    if page > page_count:
        return redirect("/track/"+ str(track_id) + "/" + str(page_count))
    
    track_image = files.get_album_art(track_id)
    if track_image:
        track_image = track_image[0]

    track_audio = files.get_track_audio(track_id)
    if track_audio:
        track_audio = track_audio[0]

    return render_template(
        "show_track.html",
        track=track,
        track_tags=track_tags,
        track_comments=track_comments,
        track_image=track_image,
        track_audio=track_audio,
        user=user,
        page=page,
        page_count=page_count
    )

@app.route("/search")
@app.route("/search/<int:page>")
def search(page=1):
    query = request.args.get("query")
    page_size = 10
    amount = tracks.find_items_amount(query)
    page_count = math.ceil(amount[0][0] / page_size)
    page_count = max(page_count, 1)

    if query:
        if page < 1:
            return redirect("/search/1?query=" + query)
        if page > page_count:
            return redirect("/search/" + str(page_count) + "?query=" + query)
            #return redirect("/" + str(page_count))
        
        
        result = tracks.find_items_paged(query,page, page_size)
        
    else:
        return redirect("/")
        #query = ""
        #result = []
    return render_template("search.html", query=query, result=result, amount=amount, page=page, page_count=page_count)

@app.route("/register")
def register():
    require_logout()
    return render_template("register.html")

@app.route("/create_account", methods=["POST"])
def create_account():
    require_logout()
    username = request.form["username"]
    if not username:
        flash("ERROR: Please enter a username")
        return redirect("/register")
    if re.search(r"\s", username):
        flash("ERROR: Whitespaces are not allowed in usernames")
        return redirect("/register")
    if len(username) > 30:
        flash("ERROR: Username cannot be longer that 30 characters")
        return redirect("/register")
    if len(username) < 3:
        flash("ERROR: Username cannot be shorter than 3 characters")
        return redirect("/register")
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("ERROR: passwords do not match")
        return redirect("/register")

    try:
        users.create_user(username, password1)

    except:
        flash("ERROR: The username is already in use")
        return redirect("/register")

    return redirect("/login?success=True")

@app.route("/edit_user/<int:user_id>")
def edit_user(user_id):
    require_login()
    if session["user_id"] != user_id:
        abort(403)
    user = users.get_user(user_id)

    return render_template("edit_user.html", user=user)

@app.route("/update_user", methods=["POST"])
def update_user():
    require_login()
    check_csrf()

    user_id = request.form["user_id"]
    image = request.files["image"]
    if image:
        valid_image = files.check_image(image)

        if valid_image[0] is not True:
            return redirect("/edit_user/" + str(user_id))

        files.save_image(valid_image[1], valid_image[2])
        image_id = db.last_insert_id()

        users.update_pfp(user_id, image_id)

    return redirect("/user/" + str(user_id))



@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        success = request.args.get("success") == "True"
        
        return render_template("login.html", success=success)
        

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username,password)

        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("ERROR: wrong username or password")
            return redirect("/login")

@app.route("/logout")
def logout():
    require_login()
    if "user_id" in session:
        del session["username"]
        del session["user_id"]
        del session["csrf_token"]
    return redirect("/")

@app.route("/new_track")
def new_track():
    require_login()
    return render_template("new_track.html")

@app.route("/create_track", methods=["POST"])
def create_track():
    require_login()
    check_csrf()


    title = request.form["title"]
    if len(title) > 50:
        flash("ERROR: Title too long (max 50 characters)")
        return redirect("/new_track")

    if not title:
        flash("ERROR: Please insert a title")
        return redirect("/new_track")

    desc = request.form["desc"].replace("\r\n", "\n")
    if len(desc) > 1000:
        flash("ERROR: Description too long (max 1000 characters)")
        return redirect("/new_track")

    track_tags = request.form["tags"]
    if len(track_tags) > 150:
        flash("ERROR: Total length of tags too long (max 150 characters)")
        return redirect("/new_track")


    taglist = tags.parse_tags(track_tags)
    if not taglist:
        flash("ERROR: Please insert at least 1 tag for your track")
        return redirect("/new_track")


    image = request.files["image"]
    if not image:
        flash("ERROR: Please insert an image for your track")
        return redirect("/new_track")

    valid_image = files.check_image(image)

    if valid_image[0] is not True:
        return redirect("/new_track")

    files.save_image(valid_image[1], valid_image[2])
    image_id = db.last_insert_id()

    audio = request.files["audio"]
    if not audio:
        flash("ERROR: Please insert an audio file for your track")
        return redirect("/new_track")

    valid_audio = files.check_audio(audio)

    if valid_audio[0] is not True:
        return redirect("/new_track")

    files.save_audio(valid_audio[1], valid_audio[2])
    audio_id = db.last_insert_id()

    user_id = session["user_id"]

    tracks.add_item(title,desc,user_id)
    track_id = db.last_insert_id()
    tags.create_tags(taglist)
    tags.assign_tags(track_id, taglist)
    files.set_album_art(track_id, image_id)
    files.set_track_audio(track_id, audio_id)

    return redirect("/track/" + str(track_id))

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
    if track_image:
        track_image = track_image[0]

    track_audio = files.get_track_audio(track_id)
    if track_audio:
        track_audio = track_audio[0]

    return render_template(
        "edit_track.html", 
        track=track,
        track_tags=track_tags,
        track_image=track_image,
        track_audio=track_audio
    )

@app.route("/update_track", methods=["POST"])
def update_track():
    require_login()
    check_csrf()
    
    image_id = None
    audio_id = None
    track_id = request.form["track_id"]

    track = tracks.get_item(track_id)
    if not track:
        abort(404)
    if session["user_id"] != track["user_id"]:
        abort(403)

    title = request.form["title"]
    if len(title) > 50:
        #abort(403)
        flash("ERROR: Title too long (max 50 characters)")
        return redirect("/edit_track/" + str(track_id))
    if not title:
        flash("ERROR: Please insert a title")
        return redirect("/edit_track/" + str(track_id))
    desc = request.form["desc"]
    if len(desc) > 1000:
        flash("ERROR: Description too long (max 1000 characters)")
        return redirect("/edit_track/" + str(track_id))
        #abort(403)
    track_tags = request.form["tags"]
    if len(track_tags) > 150:
        #abort(403)
        flash("ERROR: Total length of tags too long (max 150 characters)")
        return redirect("/edit_track/" + str(track_id))
    taglist = tags.parse_tags(track_tags)
    if not taglist:
        flash("ERROR: Please insert at least 1 tag for your track")
        return redirect("/edit_track/" + str(track_id))

    image = request.files["image"]
    if image:
        valid_image = files.check_image(image)

        if valid_image[0] is not True:
            return redirect("/edit_track/" + str(track_id))

        files.save_image(valid_image[1], valid_image[2])
        image_id = db.last_insert_id()

    audio = request.files["audio"]
    if audio:
        valid_audio = files.check_audio(audio)

        if valid_audio[0] is not True:
            return redirect("/edit_track/" + str(track_id))

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
        check_csrf()
        if "remove" in request.form:
            tags.remove_track_tags(track_id)
            comments.delete_track_comments(track_id)
            files.remove_album_art(track_id)
            files.remove_track_audio(track_id)
            tracks.remove_item(track_id)

            return redirect("/")

        return redirect("/track/" + str(track_id))

@app.route("/track/<int:track_id>/create_comment", methods=["POST"])
def create_comment(track_id):
    require_login()
    check_csrf()

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
    check_csrf()

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
    check_csrf()

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
