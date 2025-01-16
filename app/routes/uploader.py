from flask import redirect,request
import functions.utils as utils
import firebase_db, uuid
import json, time
def uploader():
    if request.method == "POST":
        quiz_data = request.json["data"]
        filename = ""
        file_is_temporary = request.json["temporary"] == "True"
        if not file_is_temporary:
            filename = request.json["name"]
            collection = "quizCollection"
        else:
            filename = str(uuid.uuid1())
            collection = "tempCollection"
        
            
        #print(term)
        #utils.save_json(term, filename)
        quiz_to_save = {
            "user": "0",
            "time_created": str(time.time()),
            "quiz_data": quiz_data
        }
        firebase_db.upload_quiz(filename, quiz_to_save, collection)
        return filename
    if request.method == "GET":
        filename = request.args.get("filename_to_get")
        file_is_temporary = request.args.get("file_is_temporary") == True
        if not file_is_temporary:
            collection = "quizCollection"
        else:
            collection = "tempCollection"
        #print(filename)
        #new_json = utils.load_json(filename)
        quiz_data = firebase_db.download_quiz(filename,collection)["quiz_data"]
        return str(json.dumps(quiz_data))