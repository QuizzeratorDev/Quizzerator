from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms
import api.firebase_db as firebase_db
import flask, uuid
from flask import session, request
def _on_leave(data):

#This joins the room, and adds session data: not host, room id
    username = data['username']
    room = data['room']
    leave_room(room)
    emit("toast_messages", {"data": username + ' has left the room.'}, to=room)