import db
from werkzeug.security import generate_password_hash, check_password_hash
import time

def get_user(user_id):
    sql = """SELECT users.id,
                    users.username,
                    users.creation_time,
                    pfp.image_id
            FROM users
            LEFT JOIN profile_photos AS pfp
            ON pfp.user_id = users.id
            WHERE users.id = ?"""
    result = db.query(sql,[user_id])
    return result[0] if result else None

def get_items(user_id):
    sql = """SELECT t.id AS track_id, t.title AS track_title, u.username AS username, u.id AS user_id, i.id AS image_id
    FROM tracks AS t
    JOIN album_arts AS a
    ON a.track_id = t.id
    JOIN images AS i
    ON i.id = a.image_id
    JOIN users AS u
    on t.user_id = u.id
    WHERE t.user_id = ?
    ORDER BY t.id DESC"""
    return db.query(sql,[user_id])

def create_user(username, password1):
    password_hash = generate_password_hash(password1)
    current_unixmills = int(time.time() * 1000)
    sql = "INSERT INTO users (username, password_hash, creation_time) VALUES (?, ?, ?)"
    db.execute(sql, [username, password_hash, current_unixmills])

def check_login(username,password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None
    password_hash = result[0]["password_hash"]
    user_id = result[0]["id"]

    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None

def update_pfp(user_id, image_id):
    sql = "DELETE FROM profile_photos WHERE user_id = ?"
    db.execute(sql,[user_id])

    sql = "INSERT INTO profile_photos (image_id, user_id) VALUES (?, ?)"
    db.execute(sql,[image_id, user_id])