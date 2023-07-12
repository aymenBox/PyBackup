from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_cors import CORS
import flask_socketio


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app,cors_allowed_origins="*")

#list of comptures
computers = []  

@app.route('/')
def index():
    return render_template('index.html', computers=computers)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('agent_executed')
def handle_agent_executed(data):
    computer = data
    computers.append(computer)
    socketio.emit('update_list_devices', {'device': computers[-1]})
    print(f'new list of computers: {computers}')
    print(f'Agent executed on {computer}')

#@socketio.on("update_list_computers")
#def handle_update_list_computers(data):
#    print(data)
#    computers = data

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8088)
