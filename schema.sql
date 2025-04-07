CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
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
    track_id INTEGER REFERENCES tracks

);

CREATE TABLE profile_photos (
    id INTEGER PRIMARY KEY,
    image_id INTEGER REFERENCES images,
    user_id INTEGER REFERENCES users

);

CREATE TABLE audios (
    id INTEGER PRIMARY KEY,
    audio BLOB,
    audio_type TEXT
);

CREATE TABLE track_audios (
    id INTEGER PRIMARY KEY,
    audio_id INTEGER REFERENCES audios,
    track_id INTEGER REFERENCES tracks
);


