from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms
import api.firebase_db as firebase_db
import flask, uuid
from flask import session, request
def _on_create(data):

#This joins the room, and adds session data: not host, room id
    number_of_questions_ = len(session["host_live_quiz_data"]["quiz_data"].keys())
    session_user = session["user"]["display_name"]
    new_data = {
        "display_name": session_user,
        "sid": request.sid,
    }
    
    room_id = str(uuid.uuid1())[:7]
    session["live_quiz_data"] = {
        "room_id": room_id,
        "host": True
    }
    join_room(room_id)
    print(room_id)
    firebase_db.upload_data(room_id, {"host": new_data, "users": []})
    
    #print(socketio.server.manager.rooms["/"]["room123"])
    emit("room_creation_data", {"data": room_id})
    emit("toast_messages", {"data": "Room created"}, to=room_id)