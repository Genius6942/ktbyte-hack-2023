from aiohttp import web
import socketio
from player import Player
from room import Room, generate_room_id
from flask import Flask, send_file

## creates a new Async Socket IO Server
sio = socketio.AsyncServer(cors_allowed_origins='*')
## Creates a new Aiohttp Web Application
app = web.Application()
# app = Flask(__name__)
# Binds our Socket.IO server to our Web App
## instance
# app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
sio.attach(app)

## we can define aiohttp endpoints just as we normally
## would with no change
async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

sockets: list = []

@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    sockets.append({
      'sid': sid,
		})

@sio.on('init')
async def init(sid, data):
	if data['name'] == '':
		sio.emit('server-error', {'message': 'Name cannot be empty'}, room=sid)
		return
	socket = get_socket(sid)
	if socket == None:
		await sio.emit('server-error', {'message': 'Socket not found'}, room=sid)
		return
	player = Player(sid, data['name'])
	socket['player'] = player
	print('new player connected: ' + player.name)

@sio.on('join')
async def join(sid, data):
	if not sid in map(lambda x: x['sid'], sockets):
		return
	room = get_room(data['room'])
	if (room == None):
		await sio.emit('server-error', {'message': 'Room not found'}, room=sid)
		print('failed to join to room', data['room'], 'because it does not exist')
		return
	else:
		await room.add_player(get_socket(sid)['player'])
		print('player joined room: ' + room.id)
        
@sio.on('create')
async def create(sid, data):
	if not sid in map(lambda x: x['sid'], sockets):
		return
	room = Room(generate_room_id(map(lambda room: room.id, rooms)), sio, data['topic'])
	await room.add_player(get_socket(sid)['player'])
	rooms.append(room)
	print('new room created: ' + room.id)

    
rooms: list[Room] = []

def get_socket(sid):
	for socket in sockets:
		if socket['sid'] == sid:
			return socket
	return None

def get_room(id):
	for room in rooms:
		if room.id == id:
			return room
	return None



## We bind our aiohttp endpoint to our app
## router
app.router.add_get('/', index)
# @app.route('/')
# def index():
#     return send_file('index.html')

## We kick off our server
if __name__ == '__main__':
    web.run_app(app)
    # app.run(host='0.0.0.0', port=8080, debug=True)