import db

def add_item(title,descr,user_id):
    sql = """INSERT INTO tracks (title, descr, user_id)
             VALUES (?, ?, ?)"""
    db.execute(sql,[title,descr,user_id])

def get_items(maara):
    sql = """SELECT id, title FROM tracks ORDER BY id DESC LIMIT ?"""
    return db.query(sql,[maara])

def get_item(item_id):
    sql = """SELECT tracks.title,
                    tracks.descr,
                    tracks.user_id,
                    users.username
            FROM tracks, users
            WHERE tracks.user_id = users.id AND
            tracks.id = ?"""
    return db.query(sql,[item_id])[0]
