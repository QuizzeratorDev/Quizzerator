
import api.firebase_db as firebase_db

from flask import redirect,request,render_template, session
def search():
    if request.method == "GET":
        query = request.args.get("search_query")
        user = request.args.get("search_user")
        if query != "":
            if user == "all":
                return firebase_db.search_documents("quizCollection", request.args.get("search_query"))
            else:
                return firebase_db.search_documents("quizCollection", request.args.get("search_query"), session["user"]["uid"])
        else:
            if user == "all":
                return firebase_db.get_all_documents("quizCollection")
            else:
                return firebase_db.get_all_documents("quizCollection", session["user"]["uid"])