from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms
import api.firebase_db as firebase_db
import flask, uuid
from flask import session, request
def _on_end_answers():

#This joins the room, and adds session data: not host, room id
    room = session["live_quiz_data"]["room_id"]
    is_host = session["live_quiz_data"]["host"]
    if is_host:
        live_quiz_data = session["host_live_quiz_data"]
        live_quiz_room_data = firebase_db.download_data(room)


        question_num = live_quiz_data["question_num"]
        question_data = live_quiz_room_data["question_" + str(question_num)]
        
        actual_question_data = live_quiz_data["quiz_data"][str(question_num)]
        
        
        
        answers = question_data["answers"]
        if not "answers" in question_data:
            return
        for answer_sid in answers.keys():
            answer = answers[answer_sid]
            is_correct = answer["answer"]  == actual_question_data[1]

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
            for user_sid in users.keys():
                if user_sid == answer_sid:
                    user = users[user_sid]
                    user["points"] += points
                    current_points = user["points"]
                    break
            
            emit("reveal_answer", {"data": {
                "valid": is_correct,
                "answer": actual_question_data[1],
                "points_gained": points,
                "current_points": current_points,
            }}, to=answer_sid)

            
        firebase_db.update_data(room, "users", users)

        #emit("reveal_all_answers", {"data": {
        #    "answers": output

        #}}, to=room)
        session["host_live_quiz_data"]["question_num"] += 1