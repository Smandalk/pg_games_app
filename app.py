from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room
import random, os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Keep track of room hosts
room_hosts = {}

@app.route('/game/<room>')
def game(room):
    return render_template('index.html', room=room)

@socketio.on('join')
def handle_join(data):
    room = data['room']
    sid = data['sid']  # unique socket id of client

    join_room(room)

    # If no host assigned yet, this player becomes the host
    if room not in room_hosts:
        room_hosts[room] = sid
        emit('host_status', {'is_host': True})
        emit('message', {'msg': f"You are the host of room {room}"}, to=sid)
    else:
        emit('host_status', {'is_host': False})
        emit('message', {'msg': f"Joined room {room}"}, to=sid)

@socketio.on('generate_number')
def handle_generate_number(data):
    room = data['room']
    sid = data['sid']

    # Only host can generate
    if room_hosts.get(room) == sid:
        number = random.randint(1, 100)
        emit('new_number', {'number': number}, room=room)
    else:
        emit('message', {'msg': "Only the host can generate numbers!"}, to=sid)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
