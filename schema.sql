CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
CREATE TABLE tracks (id SERIAL PRIMARY KEY, artist TEXT, track TEXT, genre TEXT, date TIMESTAMP);
CREATE TABLE tracks_bought (id SERIAL PRIMARY KEY, user_id TEXT, track_id TEXT);
