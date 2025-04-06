import db

def add_item(title,descr,user_id):
    sql = """INSERT INTO tracks (title, descr, user_id)
             VALUES (?, ?, ?)"""
    db.execute(sql,[title,descr,user_id])

def get_items(maara):
    sql = """SELECT tracks.id, tracks.title, users.username, users.id AS user_id, images.id AS image_id
    FROM tracks
    JOIN users
    ON tracks.user_id = users.id
    JOIN album_arts
    ON tracks.id = album_arts.track_id
    JOIN images
    ON album_arts.image_id = images.id
    ORDER BY tracks.id DESC
    LIMIT ? """
    return db.query(sql,[maara])

def get_item(item_id):
    sql = """SELECT tracks.id,
                    tracks.title,
                    tracks.descr,
                    tracks.user_id,
                    users.username
            FROM tracks, users
            WHERE tracks.user_id = users.id AND
            tracks.id = ?"""
    result = db.query(sql,[item_id])
    return result[0] if result else None

def update_item(title,desc,track_id):
    sql = """UPDATE tracks SET title = ?,
                                descr = ?
                            WHERE id = ?"""
    db.execute(sql,[title,desc,track_id])


def remove_item(track_id):
    sql = "DELETE FROM tracks WHERE id = ?"
    db.execute(sql,[track_id])

def find_items(query):
    sql = """SELECT id,title
            FROM TRACKS
            WHERE title LIKE ? OR descr LIKE ?
            ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql,[like,like])
