import firebase_admin
from firebase_admin import auth
import firebase_db
from flask import redirect,request,render_template, url_for, session, jsonify

def authenticate():
    if request.json["mode"] == "signup":
        email = request.json["email"]
        password = request.json["password"]
        user = auth.create_user(email=email, password=password)
        return jsonify({"message": "User created successfully", "uid": user.uid})
    

#auth.create_user_with_email_and_password(email, password)

#https://www.youtube.com/watch?v=HltzFtn9f1c