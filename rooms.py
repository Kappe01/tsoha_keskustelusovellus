from db import db
from flask import session
import users

def get_rooms():
    sql = "SELECT roomname FROM rooms ORDER BY id"
    result = db.session.execute(sql)
    return result.fetchall()

def new_room(roomname):
    sql = "INSERT INTO rooms (roomname) VALUES (:roomname)"
    db.session.execute(sql, {"roomname":roomname})
    db.session.commit()

    return True

def room_id():
    return session.get("room_id", 0)