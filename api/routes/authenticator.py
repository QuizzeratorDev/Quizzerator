
from firebase_admin import auth
from flask import redirect,request,render_template, url_for, session, jsonify

def authenticate():
    if request.json["mode"] == "signup":
        email = request.json["email"]
        password = request.json["password"]
        user = auth.create_user(email=email, password=password)
        return jsonify({"message": "User created successfully", "uid": user.uid})
    if request.json["mode"] == "signin":
        userinfo = request.json["userinfo"]
        print(userinfo["user"]["uid"])
        session["user"] = {
            "email": userinfo["user"]["email"],
            "uid": userinfo["user"]["uid"]
        }
        return jsonify({"message": "success"})
    if request.json["mode"] == "signout":
        session.pop("user", None)
    
    if request.json["mode"] == "getsessioninfo":
        return session["user"]

#auth.create_user_with_email_and_password(email, password)

#https://www.youtube.com/watch?v=HltzFtn9f1c