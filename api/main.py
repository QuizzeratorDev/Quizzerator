from flask import Flask, render_template,request, redirect
import api.routes.quiz
import api.routes.uploader
import api.routes.quiz_master
import api.routes.index
import api.routes.quiz_searcher
import api.routes.authenticator
import api.routes.login_page
import api.scheduler_tasks.clear_database
import api.firebase_db as firebase_db
from apscheduler.schedulers.background import BackgroundScheduler

firebase_db.setup()

app = Flask(__name__)
scheduler = BackgroundScheduler()

@app.route('/', endpoint="index")
def index():
    return api.routes.index.load_index()

@app.route("/uploader", methods = ["GET", "POST"])
def upload_file():
    return api.routes.uploader.uploader()

@app.route("/quiz", methods=["POST"])
def gen_quiz():
    return api.routes.quiz.generate_quiz()

@app.route("/quiz_master", methods=["GET", "POST"])
def mark_question():
    return api.routes.quiz_master.mark_question()

@app.route("/quiz_searcher", methods=["GET", "POST"])
def quiz_search():
    return api.routes.quiz_searcher.search()

@app.route("/authenticator", methods=["GET", "POST"])
def authenticateuser():
    return api.routes.authenticator.authenticate()

@app.route("/login", methods=["GET", "POST"])
def loginpage():
    return api.routes.login_page.display_login_page()

def clear_database_task():
    api.scheduler_tasks.clear_database.clear()

if __name__ == "__main__":
    
    scheduler.add_job(clear_database_task, 'interval', seconds=15)
    scheduler.start()
    app.run(debug=True)