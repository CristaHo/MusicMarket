CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);
CREATE TABLE tracks (id SERIAL PRIMARY KEY, artist TEXT, track TEXT, genre TEXT, price FLOAT, date TIMESTAMP);
INSERT INTO tracks (artist, track, genre, date) VALUES ('TheArtist', 'TheTrack', 'rock', 1, NOW());
CREATE TABLE tracks_bought (id SERIAL PRIMARY KEY, user_id INTEGER, track_id INTEGER);
CREATE TABLE likes (id SERIAL PRIMARY KEY, user_id INTEGER, track_id INTEGER);
CREATE TABLE comments (id SERIAL PRIMARY KEY, user_id INTEGER, track_id INTEGER, comment TEXT)
