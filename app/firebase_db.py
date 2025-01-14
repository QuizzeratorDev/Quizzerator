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

def upload_quiz(name, data):
    global db
    doc_ref = db.collection("quizCollection").document(name)
    doc_ref.set(data)



def download_quiz(name):
    global db
    doc_ref = db.collection('quizCollection').document(name)
    doc = doc_ref.get()
    if doc.exists:
        question_data = doc.to_dict()
        return json.dumps(question_data)
    else:
        return jsonify({'error': 'Quiz not found'})
