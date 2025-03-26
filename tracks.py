import db
def add_item(title,descr,user_id):
    sql = """INSERT INTO tracks (title, descr, user_id)
             VALUES (?, ?, ?)"""
    db.execute(sql,[title,descr,user_id])