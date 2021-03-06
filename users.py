from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from db import db


def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False

    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["csrf_token"] = secrets.token_hex(16)
        return True
    return False

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()

    except:
        return False

    return login(username, password)

def logout():
    del session["user_id"]
    del session["csrf_token"]

def user_id():
    return session.get("user_id", 0)

def get_all():
    sql = "SELECT id, username FROM users ORDER BY id"
    result = db.session.execute(sql)
    return result.fetchall()
