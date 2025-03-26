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

CREATE TABLE genres (
    id INTEGER PRIMARY KEY,
    title TEXT
);

CREATE TABLE track_assigned_genres (
    id INTEGER PRIMARY KEY,
    track_id INTEGER REFERENCES tracks,
    genre_id INTEGER REFERENCES genres
);

