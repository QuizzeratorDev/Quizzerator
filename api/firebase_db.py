import firebase_admin, time
from firebase_admin import credentials
from firebase_admin import firestore, json
from flask import jsonify
from rapidfuzz import fuzz

import os
import json

db = 0
def setup():
    
    #cred_dict = json.loads(os.environ.get('FIREBASE_CREDENTIALS'))
    cred_dict="../quizzerator-firebase-adminsdk-60izn-86c8037eca.json"


    print(cred_dict)
    cred = credentials.Certificate(cred_dict)
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

def delete_quiz(name, collection):
    global db
    doc_ref = db.collection(collection).document(name)
    doc_ref.delete()

def clear_documents(collection, deadline):
    docs = db.collection(collection).stream()
    for doc in docs:
        doc_data = doc.to_dict()
        time_c = doc_data["time_created"]
        #)
        if time.time()-float(time_c) >= deadline:
            delete_quiz(doc.id, collection)
            print(f"Deleted Temporary File: {doc.id} after {time.time()-float(time_c)} seconds of existence, more than the deadline of {deadline}.")

def get_number_of_quizzes():
    collection_ref = db.collection("quizCollection")
    count_query = collection_ref.count()
    count_result = count_query.get()
    return int(round(float(count_result[0][0].value)))

def search_documents(collection, query):
    docs = db.collection(collection).stream()
    result = []
    duplicates = []
    for doc in docs:
        doc_data = doc.to_dict()
        quiz_name = doc_data["quiz_name"]
        closeness = fuzz.ratio(quiz_name, query)
        if closeness in duplicates:
            closeness -= 0.01
        duplicates.append(closeness)
        result.append({
            "closeness": closeness,
            "id": doc.id,
            "quiz_data": doc_data
        })
    #result.sort(key=lambda x: x["closeness"], reverse=True)
    output = {}
    for item in result:
        if item["closeness"] > 0:
            #This reverses the order of closeness, since jsons are sorted automatically
            output[100 - item["closeness"]] = {
                "id": item["id"],
                "data": item["quiz_data"]
            }
    return output

def get_all_documents(collection):
    docs = db.collection(collection).stream()
    result = []
    i = 0
    for doc in docs:
        doc_data = doc.to_dict()
        quiz_name = doc_data["quiz_name"]
        result.append({
            "closeness": i,
            "id": doc.id,
            "quiz_data": doc_data
        })
        i += 1
    output = {}
    for item in result:
        output[100 - item["closeness"]] = {
            "id": item["id"],
            "data": item["quiz_data"]
        }
    return output