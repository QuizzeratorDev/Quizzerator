from flask import redirect,request,render_template, url_for

def check_params():
    quiz = request.args.get("quiz", default="*")
    print(quiz)
    return render_template('index.html',
                               url_quiz_name=quiz)