import db

def add_item(title,descr,user_id):
    sql = """INSERT INTO tracks (title, descr, user_id)
             VALUES (?, ?, ?)"""
    db.execute(sql,[title,descr,user_id])

def get_items(maara):
    sql = """
    SELECT 
        tracks.id, 
        tracks.title, 
        users.username, 
        users.id AS user_id, 
        images.id AS image_id,
        track_audios.audio_id

    FROM tracks
    JOIN users
    ON tracks.user_id = users.id
    JOIN album_arts
    ON tracks.id = album_arts.track_id
    JOIN images
    ON album_arts.image_id = images.id
    JOIN track_audios
    ON tracks.id = track_audios.track_id
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
    sql = """
    SELECT 
        t.id AS track_id, 
        t.title AS track_title, 
        u.username AS username, 
        u.id AS user_id, 
        i.id AS image_id,
        track_audios.audio_id AS audio_id
    FROM tracks AS t
    JOIN users AS u
    ON t.user_id = u.id
    JOIN album_arts AS a
    ON t.id = a.track_id
    JOIN images AS i
    ON a.image_id = i.id
    JOIN track_audios
    ON t.id = track_audios.track_id
    WHERE title LIKE ? OR descr LIKE ?
    ORDER BY track_id DESC"""
    like = "%" + query + "%"
    return db.query(sql,[like,like])

def find_items_amount(query):
    sql = """
    SELECT 
        COUNT(t.id) AS amount

    FROM tracks AS t
    JOIN users AS u
    ON t.user_id = u.id
    JOIN album_arts AS a
    ON t.id = a.track_id
    JOIN images AS i
    ON a.image_id = i.id
    JOIN track_audios
    ON t.id = track_audios.track_id

    WHERE title LIKE ? OR descr LIKE ?
    ORDER BY t.id DESC"""
    like = "%" + query + "%"
    return db.query(sql,[like,like])


def find_items_paged(query, page, page_size):
    sql = """
    SELECT 
        t.id AS track_id, 
        t.title AS track_title, 
        u.username AS username, 
        u.id AS user_id, 
        i.id AS image_id,
        track_audios.audio_id AS audio_id

    FROM tracks AS t
    JOIN users AS u
    ON t.user_id = u.id
    JOIN album_arts AS a
    ON t.id = a.track_id
    JOIN images AS i
    ON a.image_id = i.id
    JOIN track_audios
    ON t.id = track_audios.track_id

    WHERE title LIKE ? OR descr LIKE ?
    ORDER BY track_id DESC
    LIMIT ? OFFSET ?"""
    like = "%" + query + "%"
    offset = page_size * (page - 1)
    return db.query(sql,[like,like, page_size, offset])