from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room
import random, os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/game/<room>')
def game(room):
    return render_template('index.html', room=room)

@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('message', {'msg': f"Joined room {room}"}, room=room)

@socketio.on('generate_number')
def handle_generate_number(data):
    room = data['room']
    number = random.randint(1, 100)
    emit('new_number', {'number': number}, room=room)

if _name_ == '__main__':
    port = int(os.environ.get("PORT", 5000))

    socketio.run(app, host='0.0.0.0', port=port)

