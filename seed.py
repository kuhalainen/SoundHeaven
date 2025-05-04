import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM tracks")
db.execute("DELETE FROM comments")
db.execute("DELETE FROM audios")
db.execute("DELETE FROM track_audios")
db.execute("DELETE FROM images")
db.execute("DELETE FROM album_arts")

user_count = 1000
track_count = 10**5
comment_count = 10**6

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

with open("test_files/example.mp3", "rb") as opened:
    mp3_data = opened.read()

with open("test_files/image.png", "rb") as opened:
    image_data = opened.read()

for i in range(1, track_count + 1):
    db.execute("INSERT INTO tracks (title, descr, user_id) VALUES (?,?,?)",
               ["track" + str(i), "track" + str(i), random.randint(1,1000)])

    db.execute("INSERT INTO audios (audio, audio_type) VALUES (?, ?)",
               [mp3_data, "mp3"])
    
    db.execute("INSERT INTO track_audios (audio_id, track_id) VALUES (?,?)",
               [i, i])
    
    db.execute("INSERT INTO images (image, img_type) VALUES (?, ?)",
               [image_data, "png"])
    
    db.execute("INSERT INTO album_arts (image_id, track_id) VALUES (?,?)",
               [i, i])
    
for i in range(1, comment_count + 1):
    db.execute("INSERT INTO comments (comment, track_id, user_id) VALUES (?,?,?)",
               ["comment" + str(i), 1, random.randint(1,1000)])


db.commit()
db.close()