from db import db
import users
import rooms

def privaterooms():
    user_id = users.user_id()
    sql = ("SELECT R.id, R.roomname"
           " FROM rooms R, private_rooms P"
           " WHERE P.room_id=R.id AND P.user_id=:user_id AND R.private=True ORDER BY P.room_id")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def add_members(members):
    room_id = rooms.room_id()
    try:
        sql = "INSERT INTO private_rooms (room_id, user_id) VALUES (:room_id, :members)"
        db.session.execute(sql, {"room_id":room_id, "members":members})
        db.session.commit()
        return True
    except:
        return False
