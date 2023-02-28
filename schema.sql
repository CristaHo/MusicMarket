CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);
CREATE TABLE tracks (id SERIAL PRIMARY KEY, artist TEXT, track TEXT, genre TEXT, price FLOAT);
INSERT INTO tracks (artist, track, genre, price) VALUES ('TheArtist', 'TheTrack', 'rock', 1);
INSERT INTO tracks (artist, track, genre, price) VALUES ('BestArtist', 'Mysong', 'dance', 1);
INSERT INTO tracks (artist, track, genre, price) VALUES ('Popband', 'TrueLove', 'pop', 1);
CREATE TABLE tracks_bought (id SERIAL PRIMARY KEY, user_id INTEGER, track_id INTEGER);
CREATE TABLE likes (id SERIAL PRIMARY KEY, user_id INTEGER, track_id INTEGER);
CREATE TABLE comments (id SERIAL PRIMARY KEY, user_id INTEGER, track_id INTEGER, comment TEXT);
