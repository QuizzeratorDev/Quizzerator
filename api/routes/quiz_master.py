from flask import redirect,request,render_template, url_for
import json
import api.functions.utils as utils
import api.firebase_db as firebase_db
def mark_question():
    if request.method == "GET":
        filename = str(request.args.get("quiz_name"))
        question = request.args.get("question")
        answer = request.args.get("answer")
        quiz_data = firebase_db.download_data(filename, "tempCollection")["quiz_data"]
        if quiz_data[int(question)-1][1] == answer:
            return json.dumps({'Output': 'Correct'})
        else:
            return json.dumps({'Output': 'Incorrect', "Answer" : quiz_data[int(question)-1][1]})
    if request.method == "POST":
        filename = request.json["filename"]
        print("Deleting quiz: " + filename)
        firebase_db.delete_data(filename, "tempCollection")