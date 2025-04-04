import db
def check_image(file):
    if file.filename.endswith(".jpg") or file.filename.endswith(".jpeg"):
        img_type = "jpg"
    elif file.filename.endswith(".png"):
        img_type = "png"
    else:
        return "VIRHE: väärä tiedostomuoto"    
    image = file.read()
    if len(image) > 1000 * 1024:
        return "VIRHE: liian suuri kuva"
    
    return (True, image, img_type)

def save_image(image, img_type):
    sql = """INSERT INTO images (image, img_type) VALUES (?, ?)"""
    db.execute(sql, [image, img_type])

def set_album_art(track_id, image_id):
    sql = """INSERT INTO album_arts (image_id,track_id) VALUES (?, ?)"""
    db.execute(sql, [image_id, track_id])

def set_profile_photo(user_id, image_id):
    sql = """INSERT INTO album_arts (image_id,user_id) VALUES (?, ?)"""
    db.execute(sql, [image_id, user_id])

def get_album_art(track_id):
    sql = f"""SELECT img.id, img.image, img.img_type
                FROM images AS img
                LEFT JOIN album_arts
                ON album_arts.image_id = img.id
                WHERE track_id = ?"""
    result = db.query(sql,[track_id])
    return result

def get_image(image_id):
    sql = f"""SELECT img.id, img.image, img.img_type
                FROM images AS img
                WHERE id = ?"""
    result = db.query(sql,[image_id])
    return result

def remove_album_art(track_id):
    sql = "DELETE FROM album_arts WHERE track_id = ?"
    db.execute(sql,[track_id])
