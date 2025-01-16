import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, json
from flask import jsonify

db = 0
def setup():
    cred = credentials.Certificate(r"C:\Users\Theo Liang\Desktop\Coding\Flask\quizzerator-firebase-adminsdk-60izn-86c8037eca.json")
    firebase_admin.initialize_app(cred)
    global db
    db = firestore.client()
    
    #data = {
    #    "task": "foo",
    #    "status": "test"
    #}

    #upload_quiz("test", data)
    #doc_ref.set(data)

    #print("Document ID:", doc_ref.id)

def upload_quiz(name, data,collection):
    global db
    doc_ref = db.collection(collection).document(name)
    doc_ref.set(data)



def download_quiz(name,collection):
    global db
    doc_ref = db.collection(collection).document(name)
    doc = doc_ref.get()
    if doc.exists:
        question_data = doc.to_dict()
        return question_data

def clear_documents(collection, deadline):
    print("clearing")
    docs = db.collection(collection).stream()
    for doc in docs:
        doc_data = doc.to_dict()
        time_c = doc_data['time_created']
        print(time_c)