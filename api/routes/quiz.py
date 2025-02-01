from flask import redirect,request,render_template, url_for
import json
import functions.utils as utils
def generate_quiz():
    output = {}
    if request.method == "POST":
        entries = json.loads(request.form.get("data"))
        quizname = str(request.form.get("name"))
        filename = str(request.form.get("filename"))
        _original_filename = str(request.form.get("original_filename"))
        terms = list(entries.keys())

        #Turns entries dictionary {term: definition} into terms dictionary {question number: term}
        for question_num in terms:
            output[str(question_num)] = entries[question_num][0]
    return render_template("quiz.html", \
                               terms_dic=output,
                               quiz_name = quizname,
                               file_name = filename,
                               original_filename = _original_filename)