CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    creation_time INTEGER
);

CREATE TABLE tracks (
    id INTEGER PRIMARY KEY,
    title TEXT,
    descr TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    title TEXT UNIQUE COLLATE NOCASE
);

CREATE TABLE track_assigned_tags (
    id INTEGER PRIMARY KEY,
    track_id INTEGER REFERENCES tracks,
    tag_id INTEGER REFERENCES tags
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    comment TEXT,
    track_id INTEGER REFERENCES tracks,
    user_id INTEGER REFERENCES users
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    image BLOB,
    img_type TEXT
);

CREATE TABLE album_arts (
    id INTEGER PRIMARY KEY,
    image_id INTEGER REFERENCES images,
    track_id INTEGER REFERENCES tracks UNIQUE

);

CREATE TABLE profile_photos (
    id INTEGER PRIMARY KEY,
    image_id INTEGER REFERENCES images,
    user_id INTEGER REFERENCES users UNIQUE

);

CREATE TABLE audios (
    id INTEGER PRIMARY KEY,
    audio BLOB,
    audio_type TEXT
);

CREATE TABLE track_audios (
    id INTEGER PRIMARY KEY,
    audio_id INTEGER REFERENCES audios,
    track_id INTEGER REFERENCES tracks UNIQUE
);

CREATE UNIQUE INDEX index_users_username ON users(username);

CREATE INDEX index_tracks_user_id ON tracks(user_id);

CREATE INDEX index_comments_track_id ON comments(track_id);

CREATE INDEX index_album_arts_track_id ON album_arts(track_id);
CREATE INDEX index_album_arts_image_id ON album_arts(image_id);

CREATE INDEX index_track_audios_track_id ON track_audios(track_id);
CREATE INDEX index_track_audios_audio_id ON track_audios(audio_id);

CREATE UNIQUE INDEX index_tags_title ON tags(title);