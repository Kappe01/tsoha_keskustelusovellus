from flask import redirect, render_template, request
from app import app
import rooms
import private_room
import messages
import users
import likes

@app.route("/")
def index():
    room_list = rooms.get_rooms()
    return render_template("index.html", rooms=room_list)

@app.route("/private_room")
def privateroom():
    room_list = private_room.privaterooms()
    return render_template("private_room.html", rooms=room_list)

@app.route("/new_room")
def new_room():
    return render_template("new_room.html")

@app.route("/delete_room")
def delete_room():
    rooms.delete_room()
    return redirect("/")

@app.route("/room_logout")
def room_logout():
    rooms.logout_room()
    return redirect("/")

@app.route("/make_room", methods=["POST"])
def make_room():

    roomname = request.form["room"]
    private = request.form["private"]

    if rooms.new_room(roomname, private):
        return redirect("/")
    return render_template("error.html", error="Ryhmän luominen epäonnistui")

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

@app.route("/new_message")
def new_message():
    return render_template("new_message.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    room_id = rooms.room_id()
    message = request.form["message"]
    if messages.send(message):
        return redirect(f"/room/{room_id}")
    return render_template("error.html", error="Lähetys epäonnistui")

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
        return redirect("/")

    return render_template("error.html", error="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
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
            return render_template("error.html",
                                   error=("Käyttäjänimen tulee olla vähintään 3 merkkiä pitkä"
                                          " ja salasana tulee olla vähintään 8 merkkiä pitkä"))

        if password1 != password2:
            return render_template("error.html", error="Salasanat eivät ole samat")

        if users.register(username, password1):
            return redirect("/")
        return render_template("error.html", error="Rekisteröinti ei onnistunut")

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
    return render_template("error.html", error="Jäsenten lisääminen ei onnistunut")
