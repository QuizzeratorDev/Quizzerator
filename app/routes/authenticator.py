import firebase_admin
import firebase_db
from flask import redirect,request,render_template, url_for, session

auth = firebase_admin.auth()

#auth.create_user_with_email_and_password(email, password)
#https://www.youtube.com/watch?v=HltzFtn9f1c