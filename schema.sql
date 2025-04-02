CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
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

