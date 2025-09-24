from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)

# Room state: host + last_number
rooms = {}

@app.route("/game/<room>")
def game(room):
    return render_template("index.html", room=room)

@socketio.on("join")
def handle_join(data):
    room = data["room"]
    sid = request.sid   # server knows unique socket id
    join_room(room)

    # initialize room if new
    if room not in rooms:
        rooms[room] = {"host": sid, "last_number": None}

    is_host = (rooms[room]["host"] == sid)

    # tell this client their role
    emit("host_status", {"is_host": is_host}, room=sid)
    emit("message", {"msg": f"A new player joined room {room}"}, room=room)

    # if there’s already a number, send it immediately to the new player
    if rooms[room]["last_number"] is not None:
        emit("new_number", {"number": rooms[room]["last_number"]}, room=sid)

@socketio.on("generate_number")
def handle_generate(data):
    room = data["room"]
    sid = request.sid

    # Only the host can generate
    if rooms[room]["host"] == sid:
        number = random.randint(1, 100)
        rooms[room]["last_number"] = number   # save latest number
        emit("new_number", {"number": number}, room=room)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
