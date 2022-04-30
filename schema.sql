CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username TEXT UNIQUE,
	password TEXT,
	admin BOOL DEFAULT false
);
CREATE TABLE rooms (
	id SERIAL PRIMARY KEY,
	roomname TEXT UNIQUE,
	private BOOL DEFAULT false,
	admin_id INTEGER REFERENCES users
);
CREATE TABLE messages (
	id SERIAL PRIMARY KEY,
	message TEXT,
	user_id INTEGER REFERENCES users,
	room_id INTEGER REFERENCES rooms,
	sent TIMESTAMP
);
CREATE TABLE likes (
	message_id INTEGER REFERENCES messages,
	user_id INTEGER REFERENCES users,
	room_id INTEGER REFERENCES rooms,
	thumbsup  BOOLEAN
);
CREATE TABLE private_rooms (
	room_id INTEGER REFERENCES rooms,
	user_id INTEGER REFERENCES users
);
