from flask import redirect,request,render_template, url_for
import json
import functions.utils as utils
import firebase_db
def mark_question():
    if request.method == "GET":
        filename = str(request.args.get("quiz_name"))
        print(filename)
        question = request.args.get("question")
        answer = request.args.get("answer")
        quiz_data = firebase_db.download_quiz(filename, "tempCollection")["quiz_data"]
        if quiz_data[str(question)] == answer:
            return json.dumps({'Output': 'Correct'})
        else:
            return json.dumps({'Output': 'Incorrect', "Answer" : quiz_data[str(question)]})
    if request.method == "POST":
        filename = request.json["filename"]
        print("Deleting quiz: " + filename)
        firebase_db.delete_quiz(filename, "tempCollection")