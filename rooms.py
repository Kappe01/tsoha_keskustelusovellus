from flask import session
from db import db
import users

def get_rooms():
    sql = "SELECT id, roomname, admin_id FROM rooms WHERE private=False ORDER BY id"
    result = db.session.execute(sql)
    return result.fetchall()

def new_room(roomname, private):
    admin_id = users.user_id()
    if private:
        sql =("WITH ins1 AS ("
              " INSERT INTO rooms (roomname, private, admin_id)"
              " VALUES (:roomname, :private, :admin_id)"
              " RETURNING id AS room_id, admin_id as user_id)"
              " INSERT INTO private_rooms (room_id, user_id)"
              " SELECT room_id, user_id FROM ins1")
        db.session.execute(sql, {"roomname":roomname, "private":private, "admin_id":admin_id})
        db.session.commit()
    else:
        sql = ("INSERT INTO rooms (roomname, private, admin_id)" 
               " VALUES (:roomname, :private, :admin_id)")
        db.session.execute(sql, {"roomname":roomname, "private":private, "admin_id":admin_id})
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

def delete_room():
    r_id = room_id()
    sql = "DELETE FROM rooms WHERE id=:r_id"
    sql_2 = "DELETE FROM private_rooms WHERE room_id=:r_id"
    sql_3 = "DELETE FROM messages WHERE room_id=:r_id"
    sql_4 = "DELETE FROM likes WHERE room_id=:r_id"
    db.session.execute(sql_4, {"r_id":r_id})
    db.session.execute(sql_3, {"r_id":r_id})
    db.session.execute(sql_2, {"r_id":r_id})
    db.session.execute(sql, {"r_id":r_id})
    db.session.commit()

def room_id():
    return session.get("room_id", 0)

def is_admin(id):
    user_id = users.user_id()
    sql = "SELECT admin_id FROM rooms WHERE id=:id AND admin_id=:user_id"
    result = db.session.execute(sql, {"id":id, "user_id":user_id})
    admin = result.fetchone()
    if admin:
        return True
    return False
