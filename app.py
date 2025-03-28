import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import tracks


app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
def index():
    recent_tracks = tracks.get_items(10)
    return render_template("index.html", items=recent_tracks)

@app.route("/track/<int:track_id>")
def show_track(track_id):
    track = tracks.get_item(track_id)
    return render_template("show_track.html",track=track)



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
    del session["username"]
    del session["user_id"]
    return redirect("/")

@app.route("/new_track")
def new_track():
    return render_template("new_track.html")

@app.route("/create_track", methods=["POST"])
def create_track():
    title = request.form["title"]
    desc = request.form["desc"]
    user_id = session["user_id"]

    tracks.add_item(title,desc,user_id)


    return redirect("/")