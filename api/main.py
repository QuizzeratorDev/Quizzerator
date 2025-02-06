#!/usr/bin/python
# run.py

from flask import Flask, render_template,request, redirect, Blueprint, send_from_directory
import api.routes.quiz as quiz
import api.routes.uploader as uploader
import api.routes.quiz_master as quiz_master
import api.routes.index as index
import api.routes.quiz_searcher as quiz_searcher
import api.routes.authenticator as authenticator
import api.routes.login_page as login_page
import api.routes.live_quiz as live_quiz
import api.routes.host_quiz as host_quiz
import api.scheduler_tasks.clear_database as clear_database
import api.firebase_db as firebase_db
from apscheduler.schedulers.background import BackgroundScheduler
from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms

import api.sockets.join as join
import api.sockets.get_room_info as get_room_info
import api.sockets.create as create
import api.sockets.leave as leave
import api.sockets.host_send_message as host_send_message
import api.sockets.host_send_question as host_send_question
import api.sockets.submit_answer as submit_answer
import api.sockets.host_end_answers as host_end_answers
import api.sockets.start_quiz as start_quiz



import subprocess
from flask import session
import uuid
import time
import dotenv

firebase_db.setup()

blueprint = Blueprint('blueprint', __name__, template_folder='../api/templates', static_folder='../api/static')
scheduler = BackgroundScheduler()
socketio = SocketIO(debug=True, cors_allowed_origins='*')


@blueprint.route('/', endpoint="index", methods=["GET", "POST"])
def index_():
    return index.load_index()

@blueprint.route("/uploader", methods = ["GET", "POST"])
def upload_file():
    return uploader.uploader()

@blueprint.route("/quiz", methods=["POST"])
def gen_quiz():
    return quiz.generate_quiz()

@blueprint.route("/quiz_master", methods=["GET", "POST"])
def mark_question():
    return quiz_master.mark_question()

@blueprint.route("/quiz_searcher", methods=["GET", "POST"])
def quiz_search():
    return quiz_searcher.search()

@blueprint.route("/authenticator", methods=["GET", "POST"])
def authenticateuser():
    return authenticator.authenticate()

@blueprint.route("/login", methods=["GET", "POST"])
def loginpage():
    return login_page.display_login_page()

@blueprint.route("/live_quiz", methods=["GET", "POST"])
def live_quiz_connect():
    return live_quiz.live_quiz_connect()


@blueprint.route("/host_quiz", methods=["GET", "POST"])
def on_host_quiz():
    return host_quiz.host_quiz_connect()


#! YAYYYYY
@blueprint.route('/api/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(blueprint.static_folder, filename)

@blueprint.route('/static/<path:filename>')
def serve_static1(filename): #!THIS IS FOR LOCAL TESTING NAHHHHHGHHHH GOING ON PROD HAHAGHAHAGGHAHAHHAHGAG
    return send_from_directory(blueprint.static_folder, filename)








@socketio.on('join')
def on_join(data):
    join._on_join(data, socketio.server.manager.rooms["/"])
        
@socketio.on("get_room_info")
def on_get_info(data):
    get_room_info._on_get_room_info(data, socketio.server.manager.rooms["/"])


@socketio.on('create')
def on_join(data):
    create._on_create(data)
    
@socketio.on('leave')
def on_leave(data):
    leave._on_leave(data)


@socketio.on("host_send_message")
def on_send_message(data):
   host_send_message._on_send_message(data)

@socketio.on("host_send_question")
def on_send_question():
    host_send_question._on_send_question()

@socketio.on("start_quiz")
def on_start_quiz():
    start_quiz._on_start_quiz()

@socketio.on("submit_answer")
def on_receive_answer(data):
    submit_answer._on_submit_answer(data)
        

@socketio.on("host_end_answers")
def on_end_answers():
    host_end_answers._on_end_answers()

def clear_database_task():
    clear_database.clear()