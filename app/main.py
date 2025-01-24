from flask import Flask, render_template,request, redirect
from routes import quiz
from routes import uploader
from routes import quiz_master
from routes import main
from routes import quiz_searcher
from routes import authenticator
from routes import login_page
from scheduler_tasks import clear_database
import firebase_db
from apscheduler.schedulers.background import BackgroundScheduler

firebase_db.setup()

app = Flask(__name__)
scheduler = BackgroundScheduler()

@app.route('/', endpoint="index")
def index():
    return main.load_index()

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