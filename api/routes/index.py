from flask import redirect,request,render_template, url_for, session

def load_index():
    quiz = request.args.get("quiz", default="*")
    logged_in = "user" in session
    username = "Not logged in"
    if logged_in:
        username = "Logged in as " + session["user"]["email"]
    return render_template('index.html',
                               url_quiz_name=quiz,
                               profilemessage = username)