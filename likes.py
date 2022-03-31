import db
import messages

def new_like(like):
    message_id = messages.message_id()
    if message_id == 0:
        return False
    sql = "INSERT INTO likes (like, message_id) VALUES (:like, :message_id)"
    db.session.execute(sql, {"like":like, "message_id":message_id})
    db.session.commit()
    return True

def get_likes():
    sql = "SELECT L.Count(*) FROM likes L, messages M WHERE L.message_id=M.id"
    result = db.session.execute(sql)
    return result.fetchone()