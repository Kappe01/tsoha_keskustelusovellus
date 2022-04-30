from db import db
import users
import rooms

def get_all():
    room_id = rooms.room_id()
    sql = ("SELECT M.message, U.username, M.sent, COUNT(L.*)-1, M.id"
           " FROM messages M, users U, rooms R, likes L"
           " WHERE L.message_id=M.id AND M.user_id=U.id AND M.room_id=R.id"
           " AND M.room_id=:room_id AND L.thumbsup=True GROUP BY M.id, U.username ORDER BY M.id")
    result = db.session.execute(sql, {"room_id":room_id})
    return result.fetchall()

def send(message):
    user_id = users.user_id()
    room_id = rooms.room_id()
    if user_id == 0 or room_id == 0:
        return False

    sql = ("WITH ins1 AS ("
           " INSERT INTO messages (message, user_id, room_id, sent)"
           " VALUES (:message,:user_id,:room_id,NOW())"
           " RETURNING id AS message_id, user_id, room_id)"
           " INSERT INTO likes (message_id, user_id, room_id, thumbsup)"
           " SELECT message_id, user_id, room_id, True FROM ins1")
    db.session.execute(sql, {"message":message, "user_id":user_id, "room_id":room_id})
    db.session.commit()
    return True
