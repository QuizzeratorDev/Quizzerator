from flask import redirect,request,render_template, url_for, session
import json

def host_quiz_connect():
    if request.method == "POST":
        data = json.loads(request.form.get("quiz_data"))
        quizname = str(request.form.get("name"))
        session["host_live_quiz_data"] = {
            "quiz_data": data,
            "quiz_name": quizname,
            "question_num": 0,
        }
    return render_template("host_quiz.html", \
                               quiz_data=data,
                               quiz_name = quizname,)
