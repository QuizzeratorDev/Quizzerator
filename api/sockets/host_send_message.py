from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms
import api.firebase_db as firebase_db
import flask, uuid
from flask import session, request
def _on_send_message(data):

#This joins the room, and adds session data: not host, room id
    message = data["message"]
    room = session["live_quiz_data"]["room_id"]
    if session["live_quiz_data"]["host"]:
        emit("receive_message_from_host", {"data": message}, to=room)