import db

#Turn tags from string format into list

def parse_tags(tags_string):
    taglist = [tag.strip() for tag in tags_string.split(",")]
    if len(taglist) > 5:
        return False
    for tag in taglist:
        if len(tag) == 0:
            return False
    return taglist



def create_tags(taglist):
    for tag in taglist:
        sql = """INSERT INTO tags (title) VALUES (?)
                ON CONFLICT(title) DO NOTHING;"""
        db.execute(sql,[tag])


def assign_tags(track_id, taglist):
    #FIND IDs OF TAGS
    tag_ids = find_ids(taglist)
    #ADD ASSIGNMENTS TO DATABASE
    for tag in tag_ids:
        sql = """INSERT INTO track_assigned_tags (track_id, tag_id) VALUES (?, ?)"""
        db.execute(sql,[track_id,tag[0]])


def find_ids(taglist):
    sql = f"""SELECT DISTINCT id,title
            FROM tags
            WHERE title = ? {"OR title = ?" * (len(taglist) - 1)}
            ORDER BY id"""
    result = db.query(sql,taglist)
    return result

def find_tags(idlist):
    sql = f"""SELECT DISTINCT id,title
        FROM tags
        WHERE id = ? {"OR id = ?" * (len(idlist) - 1)}
        ORDER BY id"""
    result = db.query(sql,idlist)
    return result

def track_tags(track_id):
    sql = """SELECT tags.title
                FROM track_assigned_tags AS assi
                LEFT JOIN tags
                ON tags.id = assi.tag_id
                WHERE track_id = ?
                ORDER BY assi.id"""
    result = db.query(sql,[track_id])
    return result

def remove_track_tags(track_id):
    sql = "DELETE FROM track_assigned_tags WHERE track_id = ?"
    db.execute(sql,[track_id])

    #CURRENTLY ONLY REMOVES FROM ASSIGNED TABLE, CAN LEAVE UNUSED TAGS IN THE DATABASE.
