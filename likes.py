from db import db
import users
import rooms

def new_like(id):
    message_id = id
    user_id = users.user_id()
    room_id = rooms.room_id()
    if message_id == 0:
        return False
    sql = "INSERT INTO likes (message_id, user_id, room_id, thumbsup) VALUES (:message_id, :user_id, :room_id, True)"
    db.session.execute(sql, {"message_id":message_id, "user_id":user_id, "room_id":room_id})
    db.session.commit()
    return True
