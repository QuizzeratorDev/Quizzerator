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
        quiz_data = json.loads(firebase_db.download_quiz(filename))
        if quiz_data[str(question)] == answer:
            return json.dumps({'Output': 'Correct'})
        else:
            return json.dumps({'Output': 'Incorrect', "Answer" : quiz_data[str(question)]})
