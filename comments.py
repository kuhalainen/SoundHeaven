import db

def create_comment(track_id, user_id, comment):
        sql = """INSERT INTO comments (comment, user_id, track_id) VALUES (?, ?, ?);"""
        db.execute(sql,[comment,user_id,track_id])

def get_track_comments(track_id):
    sql = """SELECT C.id, C.comment, C.user_id, U.username
            FROM comments as C
            JOIN users AS U
            ON C.user_id = U.id
            WHERE C.track_id = ?
            ORDER BY C.id DESC"""
    return db.query(sql,[track_id])

def get_comment(comment_id):
    sql = """SELECT id, track_id, user_id
            FROM comments
            WHERE id = ?"""
    return db.query(sql,[comment_id])[0]

def delete_comment(comment_id):
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql,[comment_id])
