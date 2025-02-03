from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms
import api.firebase_db as firebase_db
import flask, uuid, time
from flask import session, request
def _on_start_quiz():

#This joins the room, and adds session data: not host, room id
    room = session["live_quiz_data"]["room_id"]
    is_host = session["live_quiz_data"]["host"]
    if is_host:
        emit("start_quiz", to=room)
        num_of_users = len(firebase_db.download_data(room)["users"])