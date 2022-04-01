CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username TEXT UNIQUE,
	password TEXT
);
CREATE TABLE rooms (
	id SERIAL PRIMARY KEY,
	roomname TEXT UNIQUE
);
CREATE TABLE messages (
	id SERIAL PRIMARY KEY,
	message TEXT,
	room_id INTEGER REFERENCES rooms,
	user_id INTEGER REFERENCES users,
	sent TIMESTAMP
);
CREATE TABLE likes (
	id SERIAL PRIMARY KEY,
	message_id INTEGER REFERENCES messages
);
