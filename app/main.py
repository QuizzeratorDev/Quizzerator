from flask import Flask, render_template,request, redirect
from routes import quiz
from routes import uploader
import firebase_db

firebase_db.setup()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/uploader", methods = ["GET", "POST"])
def upload_file():
    return uploader.uploader()

@app.route("/quiz", methods=["POST"])
def gen_quiz():
    return quiz.generate_quiz()



if __name__ == "__main__":
    app.run(debug=True)