from flask import redirect,request, session, jsonify
import functions.utils as utils
import firebase_db as firebase_db
import uuid
import json, time
def uploader():
    if request.method == "POST":
        quiz_data = request.json["data"]
        filename = ""
        
        file_is_temporary = request.json["temporary"] == "True"
        file_is_new = False
        if not file_is_temporary:
            quiz_id = int(request.json["filename"])
            if quiz_id == -1:
                filename = str(firebase_db.get_number_of_quizzes())
                file_is_new = True
            else:
                filename = str(quiz_id)
            collection = "quizCollection"
        else:
            filename = str(uuid.uuid1())
            collection = "tempCollection"
        
        #print(term)
        #utils.save_json(term, filename)
        permitted = True
        if not file_is_new:
            user_who_created_quiz = firebase_db.download_quiz(str(quiz_id),"quizCollection")["user"]
            permitted = session["user"]["uid"] == user_who_created_quiz["uid"]
        if permitted:
            quiz_to_save = {
                "quiz_name": request.json["name"],
                "user": {
                    "uid": session["user"]["uid"],
                    "email": session["user"]["email"]
                },
                "time_created": str(time.time()),
                "quiz_data": quiz_data
            }
            firebase_db.upload_quiz(filename, quiz_to_save, collection)
            return filename
        else:
            return jsonify({"message": "Not permitted to edit"})
    if request.method == "GET":
        filename = request.args.get("filename_to_get")
        file_is_temporary = request.args.get("file_is_temporary") == True
        if not file_is_temporary:
            collection = "quizCollection"
        else:
            collection = "tempCollection"
        #print(filename)
        #new_json = utils.load_json(filename)
        quiz_data = firebase_db.download_quiz(filename,collection)
        return str(json.dumps(quiz_data))