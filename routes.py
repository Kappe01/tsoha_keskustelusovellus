from flask import redirect, render_template, request, session, abort, flash
from app import app
import rooms
import private_room
import messages
import users
import likes

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/room_list")
def room_lst():
    if rooms.room_id():
        rooms.logout_room()
    room_list = rooms.get_rooms()
    return render_template("rooms.html", rooms=room_list)

@app.route("/private_room")
def privateroom():
    if rooms.room_id():
        rooms.logout_room()
    room_list = private_room.privaterooms()
    return render_template("private_room.html", rooms=room_list)

@app.route("/new_room")
def new_room():
    if rooms.room_id():
        rooms.logout_room()
    return render_template("new_room.html")

@app.route("/delete_room")
def delete_room():
    rooms.delete_room()
    return redirect("/room_list")

@app.route("/room_logout")
def room_logout():
    if rooms.room_id():
        rooms.logout_room()
    return redirect("/room_list")

@app.route("/make_room", methods=["POST"])
def make_room():

    roomname = request.form["room"]
    private = request.form["private"]
    if len(roomname) > 30:
        flash("Ryhmän nimi tulee olla alle 30 merkkiä pitkä")
        return render_template("new_room.html")
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if rooms.new_room(roomname, private):
        return redirect("/room_list")
    flash("Ryhmän luominen epäonnistui")
    return render_template("new_room.html")

@app.route("/room/<int:id>")
def in_room(id):
    allow = False
    if rooms.is_admin(id):
        allow = True
    if allow == True:
        if rooms.login_room(id):
            message_list = messages.get_all()
            return render_template("in_room_admin.html", m=message_list)

    if rooms.login_room(id):
        msg_list = messages.get_all()
        return render_template("in_room.html", msg=msg_list)

@app.route("/private/<int:id>")
def room(id):
    allow = False
    if rooms.is_admin(id):
        allow = True

    if allow == True:
        if rooms.login_room(id):
            message_list = messages.get_all()
            return render_template("in_private_room_admin.html", m=message_list)

    if rooms.login_room(id):
        msg_list = messages.get_all()
        return render_template("in_private_room.html", msg=msg_list)

@app.route("/private_message")
def private_message():
    return render_template("private_message.html")

@app.route("/send_private_message", methods=["POST"])
def send_private_message():
    room_id = rooms.room_id()
    message = request.form["msg"]
    if len(message) > 300:
        flash("Viestin tulee olla alle 300 merkkiä pitkä")
        return render_template("new_message.html")
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if messages.send(message):
        return redirect(f"/private/{room_id}")
    flash("Lähetys epäonnistui")
    return render_template("new_message.html")

@app.route("/like_private/<int:id>")
def like_private(id):
    room_id = rooms.room_id()
    likes.new_like(id)
    return redirect(f"/private/{room_id}")

@app.route("/new_message")
def new_message():
    return render_template("new_message.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    room_id = rooms.room_id()
    message = request.form["msg"]
    if len(message) > 300:
        flash("Viestin tulee olla alle 300 merkkiä pitkä")
        return render_template("new_message.html")
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if messages.send(message):
        return redirect(f"/room/{room_id}")
    flash("Lähetys epäonnistui")
    return render_template("new_message.html")

@app.route("/like_message/<int:id>")
def like_message(id):
    room_id = rooms.room_id()
    likes.new_like(id)
    return redirect(f"/room/{room_id}")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    if users.login(username, password):
        return redirect("/room_list")
    flash("Väärä tunnus tai salasana")
    return render_template("index.html")

@app.route("/logout")
def logout():
    if rooms.room_id():
        rooms.logout_room()
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if len(username) < 3 or len(password2) < 8:
            flash("Käyttäjänimen tulee olla vähintään 3 merkkiä pitkä ja salasanan vähintään 8")
            return render_template("register.html")

        if password1 != password2:
            flash("Salasanat eivät ole samat")
            return render_template("register.html")

        if users.register(username, password1):
            return redirect("/room_list")
        flash("Rekisteröinti ei onnistunut")
        return render_template("register.html")

@app.route("/add_members", methods=["GET", "POST"])
def add_member():
    room_id = rooms.room_id()
    if request.method == "GET":
        u_list = users.get_all()
        return render_template("add_members.html", user=u_list)
    if request.method == "POST":
        members = request.form["members"]

    if private_room.add_members(members):
        return redirect(f"/private/{room_id}")
    flash("Jäsenten lisääminen ei onnistunut")
    return render_template("add_members.html")
