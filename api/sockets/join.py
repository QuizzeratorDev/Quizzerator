from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms
import api.firebase_db as firebase_db
import flask
from flask import session, request
def _on_join(data, socket_rooms):

#This joins the room, and adds session data: not host, room id
    room = data['room']
    join_room(room)
    session["live_quiz_data"] = {
        "room_id": room,
        "host": False
    }



    #Gets display name of user logged in
    session_user = session["user"]["display_name"]
    #print(request.sid)
    #print(dict(socketio.server.manager.rooms["/"]["room123"]).keys()) #THIS GETS ALL SIDS IN ROOM

    new_key = request.sid
    #This is the data about to be added to room database
    new_data = {
        "display_name": session_user,
        "points": 0,
    }

    #Downloads existing room database
    room_db = firebase_db.download_data(room)
    operating_room = room in dict(socket_rooms)
    if not operating_room:
        return
    valid_room = room in firebase_db.get_all_data_keys()
    if not valid_room:
        return
    
    if "users" in room_db.keys():
        current_users = room_db["users"]

        #Checks if database room is actually an operating room

        #Gets session id of every user in operating (socketio) room
        server_room = dict(socket_rooms[room]).keys()


        for user in current_users.keys():
            #ERASES all users not in flask-socketio room (user is an sid)
            if not user in server_room:
                current_users.pop(user)
            
            #ERASES all users with the same session id, prevents someone from joining twice in same tab
            if user == request.sid:
                current_users.pop(user)
        current_users[new_key] = new_data


        #Updates room db with current users
        firebase_db.update_data(room, "users", current_users)
        all_users = current_users
        #all_users = firebase_db.download_quiz(room, "liveRooms")

        #Sends room data to all users
        emit("room_data", {"data": all_users}, to=room)
        emit("toast_messages", {"data": session_user + ' has entered the room.'}, to=room)
    else:
        firebase_db.update_data(room, "users", {
            new_key: new_data
        })
        all_users = {
            new_key: new_data
        }
            #all_users = firebase_db.download_quiz(room, "liveRooms")

        #Sends room data to all users
        emit("room_data", {"data": all_users}, to=room)
        emit("toast_messages", {"data": session_user + ' has entered the room.'}, to=room)