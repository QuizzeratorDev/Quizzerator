from flask import redirect,request
import functions.utils as utils
import firebase_db
def uploader():
    if request.method == "POST":
        quiz_data = request.json["data"]
        filename = request.json["name"]
        #print(term)
        #utils.save_json(term, filename)
        firebase_db.upload_quiz(filename, quiz_data)
        return redirect("/")
    if request.method == "GET":
        print(request.args)
        filename = request.args.get("filename_to_get")
        #print(filename)
        #new_json = utils.load_json(filename)
        quiz_data = firebase_db.download_quiz(filename)
        return str(quiz_data)