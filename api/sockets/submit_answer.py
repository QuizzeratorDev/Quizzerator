from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms
import api.firebase_db as firebase_db
import flask, uuid, time
from flask import session, request
def _on_submit_answer(data):

#This joins the room, and adds session data: not host, room id
    room = session["live_quiz_data"]["room_id"]
    display_name = session["user"]["display_name"]
    answer = data["answer"]
    sid = request.sid
    new_key = sid
    new_data = {
        "timestamp": time.time(),
        "sid":sid, 
        "display_name": display_name,
        "answer": answer
    }

    question_num = data["question_num"]

    host_sid = firebase_db.download_data(room)["host"]["sid"]

    #Adds timestamp and SID, as an answer, to question data in room db
    
    firebase_db.update_data_subsubkey(room, "question_" + str(question_num), "answers", new_key, new_data)
    room_db = firebase_db.download_data(room)
    number_of_answers = len(room_db["question_" + str(question_num)]["answers"].keys())

    emit("host_get_answers", {"data": display_name, "number_of_answers": number_of_answers}, to=host_sid)