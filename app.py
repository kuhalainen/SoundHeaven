import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import tracks


app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    recent_tracks = tracks.get_items(10)
    return render_template("index.html", items=recent_tracks)

@app.route("/track/<int:track_id>")
def show_track(track_id):
    track = tracks.get_item(track_id)
    if not track:
        abort(404)
    return render_template("show_track.html",track=track)

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
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        password_hash = result["password_hash"]
        user_id = result["id"]

        if check_password_hash(password_hash, password):
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
    user_id = session["user_id"]

    tracks.add_item(title,desc,user_id)


    return redirect("/")

@app.route("/edit_track/<int:track_id>")
def edit_track(track_id):
    require_login()
    track = tracks.get_item(track_id)
    if not track:
        abort(404)
    if session["user_id"] != track["user_id"]:
        abort(403)
    return render_template("edit_track.html", track=track)

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


    tracks.update_item(title,desc,track_id)


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
            tracks.remove_item(track_id)
            return redirect("/")
        else:
            return redirect("/track/" + str(track_id))
