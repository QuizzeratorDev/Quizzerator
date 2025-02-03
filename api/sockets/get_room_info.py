from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms
import api.firebase_db as firebase_db
import flask
from flask import session, request
def _on_get_room_info(data, socket_rooms):

#This joins the room, and adds session data: not host, room id
    #Checks if user is actually playing a live quiz
    if not "live_quiz_data" in session:
        return
        #Gets room id from session variable
    room = session["live_quiz_data"]["room_id"]

    #Gets all users currently in room
    db = firebase_db.download_data(room)
    

    #Checks if room exists in firestore
    
    if db == None:
        return
    all_users = db["users"]
    #ERASES all users not in flask-socketio room
    for user in all_users.keys():
            #ERASES all users not in flask-socketio room (user is an sid)
        if not user in dict(socket_rooms[room]).keys():
            all_users.pop(user)
    
    firebase_db.update_data(room, "users", all_users)

    #Emits room data to all users
    emit("room_data", {"data": all_users}, to=room)