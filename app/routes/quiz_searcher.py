import firebase_db
from flask import redirect,request,render_template, url_for
def search():
    if request.method == "GET":
        return firebase_db.search_documents("quizCollection", request.args.get("search_query"))