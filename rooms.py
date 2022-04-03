from flask import session
from db import db

def get_rooms():
    sql = "SELECT id, roomname FROM rooms ORDER BY id"
    result = db.session.execute(sql)
    return result.fetchall()

def new_room(roomname):
    sql = "INSERT INTO rooms (roomname) VALUES (:roomname)"
    db.session.execute(sql, {"roomname":roomname})
    db.session.commit()

    return True

def login_room(id):
    sql = "SELECT id FROM rooms WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    room = result.fetchone()
    if not room:
        return False
    session["room_id"] = room.id
    return True

def logout_room():
    del session["room_id"]

def room_id():
    return session.get("room_id", 0)
