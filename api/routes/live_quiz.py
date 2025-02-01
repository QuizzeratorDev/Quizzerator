from flask import redirect,request,render_template, url_for

def live_quiz_connect():
    return render_template("live_quiz.html")