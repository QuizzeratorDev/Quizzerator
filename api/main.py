#!/usr/bin/python
# run.py

from flask import Flask, render_template,request, redirect
import routes.quiz as quiz
import routes.uploader as uploader
import routes.quiz_master as quiz_master
import routes.index as index
import routes.quiz_searcher as quiz_searcher
import routes.authenticator as authenticator
import routes.login_page as login_page
import routes.live_quiz as live_quiz
import routes.host_quiz as host_quiz
import scheduler_tasks.clear_database as clear_database
import firebase_db as firebase_db
from apscheduler.schedulers.background import BackgroundScheduler
from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms

import subprocess
from flask import session
import uuid
import time


firebase_db.setup()

app = Flask(__name__)
app.secret_key = "6BtdCaEka6xjV4DVNxZ3pZB8mXJ70sig"
scheduler = BackgroundScheduler()
socketio = SocketIO(app,debug=True,cors_allowed_origins='*')


@app.route('/', endpoint="index", methods=["GET", "POST"])
def index_():
    return index.load_index()

@app.route("/uploader", methods = ["GET", "POST"])
def upload_file():
    return uploader.uploader()

@app.route("/quiz", methods=["POST"])
def gen_quiz():
    return quiz.generate_quiz()

@app.route("/quiz_master", methods=["GET", "POST"])
def mark_question():
    return quiz_master.mark_question()

@app.route("/quiz_searcher", methods=["GET", "POST"])
def quiz_search():
    return quiz_searcher.search()

@app.route("/authenticator", methods=["GET", "POST"])
def authenticateuser():
    return authenticator.authenticate()

@app.route("/login", methods=["GET", "POST"])
def loginpage():
    return login_page.display_login_page()

@app.route("/live_quiz", methods=["GET", "POST"])
def live_quiz_connect():
    return live_quiz.live_quiz_connect()


@app.route("/host_quiz", methods=["GET", "POST"])
def on_host_quiz():
    return host_quiz.host_quiz_connect()





@socketio.on("client_data")
def test_message(data):
    print("Received" + str(data))
    emit('server_data', {'data': "123"})


@socketio.on('join')
def on_join(data):

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


    #This is the data about to be added to room database
    new_data = {
        "display_name": session_user,
        "sid": request.sid,
        "points": 0,
        }

    #Downloads existing room database
    room_db = firebase_db.download_quiz(room, "liveRooms")
    if room in firebase_db.get_all_keys("liveRooms"):
        current_users = room_db["users"]

        #Checks if database room is actually an operating room
        if room in dict(socketio.server.manager.rooms["/"]):

            #Gets session id of every user in operating (socketio) room
            server_room = dict(socketio.server.manager.rooms["/"][room]).keys()


            for user_num in range(len(current_users)-1, -1, -1):
                user = current_users[user_num]
                #ERASES all users not in flask-socketio room
                if not user["sid"] in server_room:
                    current_users.remove(user)
                
                #ERASES all users with the same session id, prevents someone from joining twice in same tab
                if user["sid"] == request.sid:
                    current_users.remove(user)
            current_users.append(new_data)


            #Updates room db with current users
            firebase_db.update_quiz(room, "users", current_users, "liveRooms")
            all_users = current_users
            #all_users = firebase_db.download_quiz(room, "liveRooms")

            #Sends room data to all users
            emit("room_data", {"data": all_users}, to=room)
            emit("toast_messages", {"data": session_user + ' has entered the room.'}, to=room)

@socketio.on("get_room_info")
def on_get_info(data):
    #Checks if user is actually playing a live quiz
    if "live_quiz_data" in session:

        #Gets room id from session variable
        room = session["live_quiz_data"]["room_id"]

        #Gets all users currently in room
        all_users = firebase_db.download_quiz(room, "liveRooms")["users"]

        #Checks if room exists in firestore
        if firebase_db.download_quiz(room, "liveRooms") != None:
            #ERASES all users not in flask-socketio room
            for user_num in range(len(all_users)-1, -1, -1):
                
                user = all_users[user_num]
                server_room = dict(socketio.server.manager.rooms["/"][room]).keys()
                if not user["sid"] in server_room:
                    all_users.remove(user)
            firebase_db.update_quiz(room, "users", all_users, "liveRooms")

            #Emits room data to all users
            emit("room_data", {"data": all_users}, to=room)




@socketio.on('create')
def on_join(data):
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
    firebase_db.upload_quiz(room_id, {"host": new_data, "users": []}, "liveRooms")
    
    #print(socketio.server.manager.rooms["/"]["room123"])
    emit("room_creation_data", {"data": room_id})
    emit("toast_messages", {"data": "Room created"}, to=room_id)
    
@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit("toast_messages", {"data": username + ' has left the room.'}, to=room)


@socketio.on("host_send_message")
def on_send_message(data):
    message = data["message"]
    room = session["live_quiz_data"]["room_id"]
    if session["live_quiz_data"]["host"]:
        emit("receive_message_from_host", {"data": message}, to=room)

@socketio.on("host_send_question")
def on_send_question():
    room = session["live_quiz_data"]["room_id"]
    is_host = session["live_quiz_data"]["host"]
    if is_host:
        live_quiz_data = session["host_live_quiz_data"]
        
        question_num = live_quiz_data["question_num"]
        quiz_data = live_quiz_data["quiz_data"]
        
        quiz_len = live_quiz_data["quiz_len"]

        if question_num < quiz_len:

            current_question, answer = quiz_data[str(question_num)]
            
            firebase_db.update_quiz(room, "question_" + str(question_num), {
                "start_timestamp": time.time(),
                "answers": []
            }, "liveRooms")
            
            emit("receive_question", {"data": {
                "question_num": question_num,
                "question": current_question

            }}, to=room)
            
        else:
            quiz_end_data = firebase_db.download_quiz(room, "liveRooms")
            emit("end_quiz", {"data": quiz_end_data}, to=room)

@socketio.on("start_quiz")
def on_start_quiz():
    room = session["live_quiz_data"]["room_id"]
    is_host = session["live_quiz_data"]["host"]
    if is_host:
        emit("start_quiz", to=room)
        num_of_users = len(firebase_db.download_quiz(room, "liveRooms")["users"])

@socketio.on("submit_answer")
def on_receive_answer(data):
    room = session["live_quiz_data"]["room_id"]
    display_name = session["user"]["display_name"]
    answer = data["answer"]
    sid = request.sid
    to_add = {
        "timestamp": time.time(),
        "sid":sid, 
        "display_name": display_name,
        "answer": answer
    }

    question_num = data["question_num"]

    host_sid = firebase_db.download_quiz(room, "liveRooms")["host"]["sid"]

    #Adds timestamp and SID, as an answer, to question data in room db
    firebase_db.append_to_value_of_key_in_document(room, "question_" + str(question_num), "answers", to_add, "liveRooms")
    room_db = firebase_db.download_quiz(room, "liveRooms")
    number_of_answers = len(room_db["question_" + str(question_num)]["answers"])

    emit("host_get_answers", {"data": display_name, "number_of_answers": number_of_answers}, to=host_sid)
        

@socketio.on("host_end_answers")
def on_end_answers():
    room = session["live_quiz_data"]["room_id"]
    is_host = session["live_quiz_data"]["host"]
    if is_host:
        live_quiz_data = session["host_live_quiz_data"]
        live_quiz_room_data = firebase_db.download_quiz(room,"liveRooms")


        question_num = live_quiz_data["question_num"]
        question_data = live_quiz_room_data["question_" + str(question_num)]
        
        actual_question_data = live_quiz_data["quiz_data"][str(question_num)]
        
        
        
        answers = question_data["answers"]
        for answer in answers:
            print(actual_question_data[1])
            is_correct = answer["answer"]  == actual_question_data[1]
            answer_sid = answer["sid"]

            original_timestamp = question_data["start_timestamp"]
            timestamp = answer["timestamp"]

            difference = round(timestamp, 1) - round(original_timestamp, 1)
            #ie. 1.2 seconds

            
            points_difference = difference * 100
            #ie. 120

            if points_difference > 500:
                points_difference = 500

            points_difference = round(points_difference/4)
            points = 0

            if is_correct:
                points = 1000 - points_difference
            
            current_points = 0
            users = live_quiz_room_data["users"]
            for user in users:
                if user["sid"] == answer_sid:
                    user["points"] += points
                    current_points = user["points"]
                    break
            
            emit("reveal_answer", {"data": {
                "valid": is_correct,
                "answer": actual_question_data[1],
                "points_gained": points,
                "current_points": current_points,
            }}, to=answer_sid)

            
            firebase_db.update_quiz(room, "users", users, "liveRooms")

        #emit("reveal_all_answers", {"data": {
        #    "answers": output

        #}}, to=room)
        session["host_live_quiz_data"]["question_num"] += 1

def clear_database_task():
    clear_database.clear()

if __name__ == "__main__":
    
    scheduler.add_job(clear_database_task, 'interval', seconds=15)
    scheduler.start()
    app.run(host='0.0.0.0', port=8080)