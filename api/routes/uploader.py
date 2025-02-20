from flask import redirect,request, session, jsonify
import api.functions.utils as utils
import api.firebase_db as firebase_db
import uuid
import json, time
def uploader():
    if request.method == "POST":
        
        if not "delete_quiz" in request.json:
            quiz_data = request.json["data"]
            filename = ""
            
            file_is_temporary = request.json["temporary"] == "True"
            file_is_new = False
            if not file_is_temporary:
                quiz_id = int(request.json["filename"])
                if quiz_id == -1:
                    filename = str(uuid.uuid1())
                    file_is_new = True
                else:
                    filename = str(uuid.uuid1())
                collection = "quizCollection"
            else:
                filename = str(uuid.uuid1())
                collection = "tempCollection"
            
            #print(term)
            #utils.save_json(term, filename)
            permitted = True
            if not file_is_new and not file_is_temporary:
                user_who_created_quiz = firebase_db.download_data(str(quiz_id),"quizCollection")["user"]
                permitted = session["user"]["uid"] == user_who_created_quiz["uid"]
            if permitted:
                if not file_is_temporary:
                    quiz_to_save = {
                        "quiz_name": request.json["name"],
                        "user": {
                            "uid": session["user"]["uid"],
                            "email": session["user"]["email"],
                            "display_name": session["user"]["display_name"]
                        },
                        "time_created": str(time.time()),
                        "quiz_data": quiz_data
                    }
                else:
                    quiz_to_save = {
                        "quiz_name": request.json["name"],
                        "time_created": str(time.time()),
                        "quiz_data": quiz_data
                    }
                print(filename, quiz_to_save)
                firebase_db.upload_data(filename, quiz_to_save, collection)
                return filename
            else:
                return jsonify({"message": "Not permitted to edit"})
        elif request.json["delete_quiz"] == True:
            id_to_delete = request.json["quiz_id"]
            if id_to_delete == -1:
                return
            user_who_created_quiz = firebase_db.download_data(str(id_to_delete),"quizCollection")["user"]
            permitted = session["user"]["uid"] == user_who_created_quiz["uid"]
            if permitted:
                firebase_db.delete_data(id_to_delete, "quizCollection")
                return jsonify({"message": "Successfully deleted quiz"})
            
    if request.method == "GET":
        filename = request.args.get("filename_to_get")
        file_is_temporary = request.args.get("file_is_temporary") == True
        if not file_is_temporary:
            collection = "quizCollection"
        else:
            collection = "tempCollection"
        #print(filename)
        #new_json = utils.load_json(filename)
        quiz_data = firebase_db.download_data(filename,collection)
        return str(json.dumps(quiz_data))