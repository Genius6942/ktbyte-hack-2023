import socketio
from flask import Flask, send_file

flaskServer = Flask(__name__)

import socketio

# create a Socket.IO server
sio = socketio.Server()

# wrap with a WSGI application
app = socketio.WSGIApp(
    sio, static_files={"/": {"content_type": "text/html", "filename": "index.html"}}
)


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
def init(data):
    print(data)


# app.run(host='0.0.0.0', port=5000, debug=True)
