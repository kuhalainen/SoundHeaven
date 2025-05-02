from flask import flash
import db

def check_image(file):
    if file.filename.endswith(".jpg") or file.filename.endswith(".jpeg"):
        img_type = "jpg"
    elif file.filename.endswith(".png"):
        img_type = "png"
    else:
        flash("ERROR: Wrong image file format")
        return (False, None, None)
    image = file.read()
    if len(image) > 1000 * 1024:
        flash("ERROR: The image file is too large (Max 1MB)")
        return (False, None, None)

    return (True, image, img_type)

def save_image(image, img_type):
    sql = """INSERT INTO images (image, img_type) VALUES (?, ?)"""
    db.execute(sql, [image, img_type])

def set_album_art(track_id, image_id):
    sql = """INSERT INTO album_arts (image_id,track_id) VALUES (?, ?)"""
    db.execute(sql, [image_id, track_id])

#def set_profile_photo(user_id, image_id):
#    sql = """INSERT INTO album_arts (image_id,user_id) VALUES (?, ?)"""
#    db.execute(sql, [image_id, user_id])

def get_album_art(track_id):
    sql = """SELECT img.id, img.image, img.img_type
                FROM images AS img
                LEFT JOIN album_arts
                ON album_arts.image_id = img.id
                WHERE track_id = ?"""
    result = db.query(sql,[track_id])
    return result

def get_image(image_id):
    sql = """SELECT img.id, img.image, img.img_type
                FROM images AS img
                WHERE id = ?"""
    result = db.query(sql,[image_id])
    return result

def remove_album_art(track_id):
    image = get_album_art(track_id)
    sql = "DELETE FROM album_arts WHERE track_id = ?"
    db.execute(sql,[track_id])
    if image:
        sql = "DELETE FROM images WHERE id = ?"
        print(image)
        db.execute(sql,[image[0][0]])

def set_default_pfp(user_id):
    sql = """INSERT INTO profile_photos (user_id, image_id) VALUES (?, NULL)"""
    db.execute(sql, [user_id])

#################

def check_audio(audio):
    if not audio.filename.endswith(".mp3"):
        flash("ERROR: Wrong audio file format")
        return (False, None, None)
    audio2 = audio.read()
    print(len(audio2))
    if len(audio2) > 10000 * 1024:
        flash("ERROR: The audio file is too large (Max 10MB)")
        return (False, None, None)

    return (True, audio2, "mp3")

def save_audio(audio, file_type):
    sql = """INSERT INTO audios (audio, audio_type) VALUES (?, ?)"""
    db.execute(sql, [audio, file_type])

def set_track_audio(track_id, audio_id):
    sql = """INSERT INTO track_audios (audio_id,track_id) VALUES (?, ?)"""
    db.execute(sql, [audio_id, track_id])

def get_track_audio(track_id):
    sql = """SELECT au.id, au.audio, au.audio_type
                FROM audios AS au
                LEFT JOIN track_audios AS tr
                ON tr.audio_id = au.id
                WHERE track_id = ?"""
    result = db.query(sql,[track_id])
    return result

def get_audio(audio_id):
    sql = """SELECT au.id, au.audio, au.audio_type
                FROM audios AS au
                WHERE id = ?"""
    result = db.query(sql,[audio_id])
    return result

def remove_track_audio(track_id):
    audio = get_track_audio(track_id)
    sql = "DELETE FROM track_audios WHERE track_id = ?"
    db.execute(sql,[track_id])
    if audio:
        sql = "DELETE FROM audios WHERE id = ?"
        print(audio)
        db.execute(sql,[audio[0][0]])
