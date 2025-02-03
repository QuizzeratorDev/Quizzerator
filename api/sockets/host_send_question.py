from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms
import api.firebase_db as firebase_db
import flask, uuid, time
from flask import session, request
def _on_send_question():

#This joins the room, and adds session data: not host, room id
    room = session["live_quiz_data"]["room_id"]
    is_host = session["live_quiz_data"]["host"]
    if is_host:
        live_quiz_data = session["host_live_quiz_data"]
        
        question_num = live_quiz_data["question_num"]
        quiz_data = live_quiz_data["quiz_data"]
        
        quiz_len = live_quiz_data["quiz_len"]

        if question_num < quiz_len:

            current_question, answer = quiz_data[str(question_num)]
            
            firebase_db.update_data(room, "question_" + str(question_num), {
                "start_timestamp": time.time(),
                
            })
            
            emit("receive_question", {"data": {
                "question_num": question_num,
                "question": current_question

            }}, to=room)
            
        else:
            quiz_end_data = firebase_db.download_data(room)
            emit("end_quiz", {"data": quiz_end_data}, to=room)