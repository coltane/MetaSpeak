from flask import Flask, session
from flask_socketio import SocketIO, emit
from os import environ

app = Flask(__name__)
app.config['SECRET_KEY'] = environ['SECRET_KEY']
sio = SocketIO(app)

users = {}

# index
@app.route('/')
def index():
	return 'Nothing to see here'

# listens for a new connection
@sio.on('connection', namespace='/chat')
def user_connected(message):
	print("User connected!")

# listens for a new message, emits it to everyone connected
@sio.on('new message', namespace='/chat')
def new_message(message):
	emit('new message', {'username': session['username'], 'message': message}, broadcast=True)

# listens for a new user, emits message to everyone when new user joins
@sio.on('new user', namespace='/chat')
def add_user(username):
	global users

	if not users.get(username):
		session['username'] = username
		users[username] = session['username']
		
		emit('user joined', {'username': session['username']}, broadcast=True)

# handles disconnections
@sio.on('disconnect', namespace='/chat')
def disconnect():
	global users
	try:
		del usernames[session['username']]
		emit('user left', { 'username' : session['username'], 'numUsers' : number_of_users}, broadcast=True)
	except:
		pass

if __name__=='__main__':
	sio.run(app)
