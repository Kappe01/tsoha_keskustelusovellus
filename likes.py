from db import db
import users

def new_like(id):
    message_id = id
    user_id = users.user_id()
    if message_id == 0:
        return False
    sql = "INSERT INTO likes (message_id, user_id, thumbsup) VALUES (:message_id, :user_id, True)"
    db.session.execute(sql, {"message_id":message_id, "user_id":user_id})
    db.session.commit()
    return True
