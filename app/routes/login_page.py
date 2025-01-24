from flask import redirect,request,render_template, url_for
import firebase_db

def display_login_page():
    return render_template('login.html',
                              )