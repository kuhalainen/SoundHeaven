import db

def get_user(user_id):
    sql = """SELECT users.id,
                    users.username
            FROM users
            WHERE users.id = ?"""
    result = db.query(sql,[user_id])
    return result[0] if result else None

def get_items(user_id):
    sql = """SELECT id, title 
    FROM tracks 
    WHERE user_id = ?
    ORDER BY id DESC"""
    return db.query(sql,[user_id])