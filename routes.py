from app import app
from flask import redirect, render_template, request
import rooms, messages, users


@app.route("/")
def index():
    room_list = rooms.get_rooms()
    return render_template("index.html", rooms=room_list)

@app.route("/new_room")
def new_room():
    return render_template("new_room.html")

@app.route("/new_message")
def new_message():
    return render_template("new_message.html")

@app.route("/in_room")
def in_room():
    msg_list = messages.get_all()
    return render_template("in_room.html", msg=msg_list)

@app.route("/send_message", methods=["POST"])
def send_message():
    message = request.form["message"]
    if messages.send(message):
        return redirect("/in_room")
    else:
        return render_template("error.html", error="Lähetys epäonnistui")

@app.route("/make_room", methods=["POST"])
def make_room():
    roomname = request.form["room"]
    if rooms.new_room(roomname):
        return redirect("/")
    else:
        return render_template("error.html", error="Ryhmän luominen epäonnistui")

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    if users.login(username,password):
        return redirect("/")
    else:
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
        if len(username) < 3:
            return render_template("error.html", error="Käyttäjänimen tulee olla vähintään 3 merkkiä pitkä")
        if len(password2) < 8:
            return render_template("error.html", error="Salasana tulee olla vähintään 8 merkkiä pitkä")
        if password1 != password2:
            return render_template("error.html", error="Salasanat eivät ole samat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", error="Rekisteröinti ei onnistunut")