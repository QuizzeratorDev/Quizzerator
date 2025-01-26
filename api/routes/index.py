from flask import redirect,request,render_template, url_for

def load_index():
    quiz = request.args.get("quiz", default="*")
    
    return render_template('index.html',
                               url_quiz_name=quiz)