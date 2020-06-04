import os

from datetime import datetime
from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


app.config["SECRET_KEY"] = 'e11c5a47c7d64810c28824a784e6610f23e27aaf63157c2f'
socketio = SocketIO(app)

chatlist = []  
usernames = []  
messagedict = {}  



@app.route("/")
def index():
    
    if "user_name" in session:

        
        if "chat_id" in session:
            if len(chatlist) >= session["chat_id"]:
                return redirect(url_for('chatroom', chat_id=session["chat_id"]))

        return redirect(url_for('chatroomlist'))
    return render_template("index.html")



@app.route("/logout", methods=["GET"])
def logout():

   
    try:
        hell = session.pop("user_name")
    except KeyError:
        return render_template("error.html", error_message="Please identify yourself first")
    else:
        usernames.remove(hell)
    return redirect(url_for('index'))


@app.route("/chatrooms", methods=["GET", "POST"])
def chatroomlist():

    if request.method == "POST":
        user_name = request.form.get("user_name")
        if user_name in usernames:
            return render_template("error.html", error_message="Username already exists.")
        usernames.append(user_name)
        session["user_name"] = user_name

    if request.method=="GET" and "user_name" not in session:
        return render_template("error.html", error_message="Please identify yourself first.")

    return render_template("chatlist.html", chatlist=chatlist, user_name=session["user_name"])


@app.route("/chatrooms/<int:chat_id>", methods=["GET", "POST"])
def chatroom(chat_id):

    if request.method == "POST":
        chatroom_name = request.form.get("chatroom_name")
        if chatroom_name in chatlist:
            return render_template("error.html", error_message="The chatroom already exists.")

        chatlist.append(chatroom_name)
        messagedict[chatroom_name] = []

    if request.method == "GET":
        if "user_name" not in session:
            return render_template("error.html", error_message="Please identify yourself first.")
        if len(chatlist) < chat_id:
            return render_template("error.html", error_message="Chatroom Doesn't Exist."
                                                               " If you want the same chatroom, go back and create one")

    session["chat_id"] = chat_id

    return render_template("chatroom.html", user_name=session["user_name"])


@socketio.on("submit message")
def message(data):
    selection = data["selection"]
    time = datetime.now().strftime("%Y-%m-%d %H:%M")  

    response_dict = {"selection": selection, "time": time, "user_name": session["user_name"]}
    messagelist = messagedict[chatlist[session["chat_id"] - 1]]

    if len(messagelist) == 100:
        del messagelist[0]

    messagelist.append(response_dict)
    emit("cast message", {**response_dict, **{"chat_id": str(session["chat_id"])}}, broadcast=True)


@socketio.on("submit channel")
def submit_channel(data):

    emit("cast channel", {"selection": data["selection"], "chat_id": len(chatlist) + 1}, broadcast=True)


@app.route("/listmessages", methods=["POST"])
def listmessages():
    return jsonify({**{"message": messagedict[chatlist[session["chat_id"]-1]]}, **{"chat_id": session["chat_id"]}})


if __name__ == "__main__":
    app.run(debug=True)
