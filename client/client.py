import socketio
import platform
from pybackupUtility import System_information
import json

# Connect to the server
sio = socketio.Client()

# Define the connect event handler
@sio.on('connect')
def on_connect():
    print("getting system information ...")
    # Get the system information
    systeminformation = json.loads(System_information())
    print("system information has been collected.")
    # Send the computer name to the server
    sio.emit('agent_executed', {'system_information': systeminformation})
    print('Agent executed on', systeminformation['Node Name'])

# Define the disconnect event handler
@sio.on('disconnect')
def on_disconnect():
    print('Disconnected from the server')

# Start the connection
sio.connect('http://10.10.100.90:8088')

# Wait for events
sio.wait()
