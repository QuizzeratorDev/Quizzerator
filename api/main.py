#!/usr/bin/python
# run.py

from flask import Flask, render_template,request, redirect
import routes.quiz as quiz
import routes.uploader as uploader
import routes.quiz_master as quiz_master
import routes.index as index
import routes.quiz_searcher as quiz_searcher
import routes.authenticator as authenticator
import routes.login_page as login_page
import scheduler_tasks.clear_database as clear_database
import firebase_db as firebase_db
from apscheduler.schedulers.background import BackgroundScheduler

firebase_db.setup()

app = Flask(__name__)
app.secret_key = "6BtdCaEka6xjV4DVNxZ3pZB8mXJ70sig"
scheduler = BackgroundScheduler()

@app.route('/', endpoint="index")
def index_():
    return index.load_index()

@app.route("/uploader", methods = ["GET", "POST"])
def upload_file():
    return uploader.uploader()

@app.route("/quiz", methods=["POST"])
def gen_quiz():
    return quiz.generate_quiz()

@app.route("/quiz_master", methods=["GET", "POST"])
def mark_question():
    return quiz_master.mark_question()

@app.route("/quiz_searcher", methods=["GET", "POST"])
def quiz_search():
    return quiz_searcher.search()

@app.route("/authenticator", methods=["GET", "POST"])
def authenticateuser():
    return authenticator.authenticate()

@app.route("/login", methods=["GET", "POST"])
def loginpage():
    return login_page.display_login_page()

def clear_database_task():
    clear_database.clear()

if __name__ == "__main__":
    
    scheduler.add_job(clear_database_task, 'interval', seconds=15)
    scheduler.start()
    app.run(debug=True)