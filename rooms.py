import db
from flask import session
import users

def get_rooms():
    sql = "SELECT R.roomname FROM rooms R, users U WHERE R.user_id=U.id ORDER BY R.id"
    result = db.session.execute(sql)
    return result.fetchall()

def new_room(roomname):
    user_id = users.user_id
    if user_id == 0:
        return False
    sql = "INSERT INTO rooms (roomname, user_id) VALUES (:roomname, :user_id)"
    db.session.execute(sql, {"roomname":roomname, "user_id":user_id})
    db.session.commit()

    return True

def room_id():
    return session.get("room_id", 0)