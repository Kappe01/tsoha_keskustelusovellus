CREATE TABLE users (
	id SEREIAL PRIMARY KEY,
	username TEXT UNIQUE,
	password TEXT,
	admin BOOLEAN
);
CREATE TABLE rooms (
	id SERIAL PRIMARY KEY,
	roomname TEXT UNIQUE,
	user_id INTEGER REFERENCES users
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
	like BOOLEAN,
	message_id INTEGER REFERENCE messages
);
