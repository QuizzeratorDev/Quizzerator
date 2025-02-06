import firebase_admin, time
from firebase_admin import credentials
from firebase_admin import firestore, json, db
from flask import jsonify
from rapidfuzz import fuzz
import platform

import os
import json

import socket
from dotenv import load_dotenv

load_dotenv()
fire_store = 0
db_ref = 0
def setup():
    
    
    cred_dict = json.loads(os.environ.get('FIREBASE_CREDENTIALS', '{}'))

    print(f"Firebase Credentials Loaded!")
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://quizzerator-default-rtdb.europe-west1.firebasedatabase.app/"
    })
    global fire_store
    fire_store = firestore.client()

    global db_ref
    db_ref = db.reference("liveRooms")
    
    #data = {
    #    "task": "foo",
    #    "status": "test"
    #}

    #upload_quiz("test", data)
    #doc_ref.set(data)

    #print("Document ID:", doc_ref.id)
    print("Setup Complete!")



def download_data(name):
    global db_ref
    ref = db_ref.child(name).get()
    if ref: #exists
        return ref

def upload_data(name, data):
    print("Uploading data " + str(data))
    global db_ref
    db_ref.child(name).set(data)
    print("Finished uploading data: " + str(data))


#This is essentially a double-layered version of "append_to_document", but in realtime database
#Takes document ID, then a key of the document, then a sub_key (value), then appends new_el to that sub_key
#For instance, document ID "room109" with key "question 5" with sub_key "answers" as an array, which need to be appended
def update_data_subkey(name, key, subkey, value):
    global db_ref
    ref = db_ref.child(name)
    doc = ref.get()
    if doc: #exists
        db_ref.child(name).child(key).child(subkey).set(value)

def update_data_subsubkey(name, key, subkey, subsubkey, value):
    global db_ref
    ref = db_ref.child(name)
    doc = ref.get()
    if doc:
        db_ref.child(name).child(key).child(subkey).child(subsubkey).set(value)

def update_data(name,new_key, new_value):
    global db_ref
    doc_ref = db_ref.child(name).get()
    if doc_ref: #exists
        db_ref.child(name).child(new_key).set(new_value)


def download_data_list(name, key):
    global db_ref
    doc_ref = db_ref.child(name).get()
    if doc_ref: #exists
        db_ref.child(name).child(key).get().values()

def get_all_data_keys():
    global db_ref
    return [*db_ref.get(False, True)] #get keys as list


def upload_quiz(name, data,collection):
    global fire_store
    doc_ref = fire_store.collection(collection).document(name)
    doc_ref.set(data)

def download_quiz(name,collection):
    global fire_store
    doc_ref = fire_store.collection(collection).document(name)
    doc = doc_ref.get()
    if doc.exists:
        question_data = doc.to_dict()
        return question_data

def update_quiz(name,new_key, new_value, collection):
    global fire_store
    doc_ref = fire_store.collection(collection).document(name)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.update({new_key: new_value})

def append_to_document(name,new_key, new_value, collection):
    global fire_store
    doc_ref = fire_store.collection(collection).document(name)
    doc = doc_ref.get()
    if doc.exists:
        current_users = doc.to_dict()[new_key]
        current_users.append(new_value)
        print(current_users)
        doc_ref.update({new_key: current_users})



def delete_quiz(name, collection):
    global fire_store
    doc_ref = fire_store.collection(collection).document(name)
    doc_ref.delete()

def clear_documents(collection, deadline):
    docs = fire_store.collection(collection).stream()
    for doc in docs:
        doc_data = doc.to_dict()
        time_c = doc_data["time_created"]
        #)
        if time.time()-float(time_c) >= deadline:
            delete_quiz(doc.id, collection)
            print(f"Deleted Temporary File: {doc.id} after {time.time()-float(time_c)} seconds of existence, more than the deadline of {deadline}.")

def get_number_of_quizzes():
    collection_ref = fire_store.collection("quizCollection")
    count_query = collection_ref.count()
    count_result = count_query.get()
    return int(round(float(count_result[0][0].value)))

def search_documents(collection, query):
    docs = fire_store.collection(collection).stream()
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
    docs = fire_store.collection(collection).stream()
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

def get_all_keys(collection):
    docs = fire_store.collection(collection).stream()
    result = []
    i = 0
    for doc in docs:
        result.append(doc.id)
    return result