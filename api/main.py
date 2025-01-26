from flask import Flask, render_template,request, redirect
import routes.quiz
import routes.uploader
import routes.quiz_master
import routes.main
import routes.quiz_searcher
import routes.authenticator
import routes.login_page
import scheduler_tasks.clear_database
import firebase_db
from apscheduler.schedulers.background import BackgroundScheduler

firebase_db.setup()

app = Flask(__name__)
scheduler = BackgroundScheduler()

@app.route('/', endpoint="index")
def index():
    return routes.main.load_index()

@app.route("/uploader", methods = ["GET", "POST"])
def upload_file():
    return routes.uploader.uploader()

@app.route("/quiz", methods=["POST"])
def gen_quiz():
    return routes.quiz.generate_quiz()

@app.route("/quiz_master", methods=["GET", "POST"])
def mark_question():
    return routes.quiz_master.mark_question()

@app.route("/quiz_searcher", methods=["GET", "POST"])
def quiz_search():
    return routes.quiz_searcher.search()

@app.route("/authenticator", methods=["GET", "POST"])
def authenticateuser():
    return routes.authenticator.authenticate()

@app.route("/login", methods=["GET", "POST"])
def loginpage():
    return routes.login_page.display_login_page()

def clear_database_task():
    scheduler_tasks.clear_database.clear()

if __name__ == "__main__":
    
    scheduler.add_job(clear_database_task, 'interval', seconds=15)
    scheduler.start()
    app.run(debug=True)