import db

#Turn tags from string format into list

def parse_tags(track_tags):
    taglist = [tag.strip() for tag in track_tags.split(",")]
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
    pass
    #ADD ASSIGNMENTS TO DATABASE
    for tag in tag_ids:
        sql = """INSERT INTO track_assigned_tags (track_id, tag_id) VALUES (?, ?)"""
        db.execute(sql,[track_id,tag[0]])


def find_ids(taglist):
    sql = f"""SELECT DISTINCT id,title
            FROM tags
            WHERE title = ? {"OR title = ?" * (len(taglist) - 1)}
            ORDER BY id DESC"""
    result = db.query(sql,taglist)
    for a in result:
        print(a[0])
    return result

def find_tags(idlist):
    sql = f"""SELECT DISTINCT id,title
        FROM tags
        WHERE id = ? {"OR id = ?" * (len(idlist) - 1)}
        ORDER BY id DESC"""
    result = db.query(sql,idlist)
    for a in result:
        print(a[0])
    return result

def track_tags(track_id):
    sql = f"""SELECT tags.title
                FROM track_assigned_tags AS assi
                LEFT JOIN tags
                ON tags.id = assi.tag_id
                WHERE track_id = ?"""
    result = db.query(sql,[track_id])
    for a in result:
        print(a[0])
    return result

def remove_track_tags(track_id):
    sql = "DELETE FROM track_assigned_tags WHERE track_id = ?"
    db.execute(sql,[track_id])

    #CURRENTLY ONLY REMOVES FROM ASSIGNED TABLE, CAN POTENTIALLY LEAVE UNUSED TAGS IN THE DATABASE.
    
    
    
    
