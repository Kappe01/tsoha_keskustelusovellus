from db import db
from flask import session
import users, rooms


def get_first():
    room_id = rooms.room_id()
    sql = "SELECT M.message, U.username, M.sent, L.like FROM messages M, users U, rooms R, likes L WHERE M.user_id=U.id AND M.room_id=R.id AND L.message_id=M.id AND M.room_id=:room_id ORDER BY M.id"
    result = db.session.execute(sql, {"room_id":room_id})
    return result.fetchone()

def get_all():
    room_id = rooms.room_id()
    sql = "SELECT M.message, U.username, M.sent FROM messages M, users U, rooms R WHERE M.user_id=U.id AND M.room_id=R.id AND M.room_id=:room_id ORDER BY M.id"
    result = db.session.execute(sql, {"room_id":room_id})
    return result.fetchall()

def send(message):
    user_id = users.user_id()
    room_id = rooms.room_id()
    if user_id == 0 or room_id == 0:
        return False    
    
    sql = "INSERT INTO messages (message, user_id, room_id, sent) VALUES (:message,:user_id,:room_id,NOW())"
    db.session.execute(sql, {"message":message, "user_id":user_id, "room_id":room_id})
    db.session.commit()
    return True