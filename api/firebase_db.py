import firebase_admin, time
from firebase_admin import credentials
from firebase_admin import firestore, json, db
from flask import jsonify
from rapidfuzz import fuzz
import platform
import rapidjson
import os
import json
import random

import socket
from dotenv import load_dotenv

load_dotenv()
fire_store = 0
db_ref = 0
def setup():
    
    if platform.system() == "Darwin":  # macOS
        cred_dict = "quizzerator-firebase-sasha.json"
    else:
        cred_dict = rapidjson.loads(str(os.getenv('FIREBASE_CREDENTIALS_DICT')))
    
    cred = credentials.Certificate(cred_dict)
    print(f"Firebase Credentials Loaded!")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://quizzerator-default-rtdb.europe-west1.firebasedatabase.app/"
    })
    #global fire_store
    #fire_store = firestore.client()
    print("Setup Complete!")



def download_data(name, collection="liveRooms"):
    ref = db.reference(collection)
    docref = ref.child(name).get()
    if docref: #exists
        return docref

def upload_data(name, data, collection="liveRooms"):
    ref = db.reference(collection)
    ref.child(str(name)).set(data)


#This is essentially a double-layered version of "append_to_document", but in realtime database
#Takes document ID, then a key of the document, then a sub_key (value), then appends new_el to that sub_key
#For instance, document ID "room109" with key "question 5" with sub_key "answers" as an array, which need to be appended
def update_data_subkey(name, key, subkey, value):
    global db_ref
    ref = db_ref.child(name)
    doc = ref.get()
    if doc: #exists
        db_ref.child(name).child(key).child(subkey).set(value)

def update_data_subsubkey(name, key, subkey, subsubkey, value, collection="liveRooms"):
    db_ref = db.reference(collection)
    ref = db_ref.child(name)
    doc = ref.get()
    if doc:
        db_ref.child(name).child(key).child(subkey).child(subsubkey).set(value)

def update_data(name,new_key, new_value, collection="liveRooms"):
    db_ref = db.reference(collection)
    doc_ref = db_ref.child(name).get()
    if doc_ref: #exists
        db_ref.child(name).child(new_key).set(new_value)

def delete_data(name, collection="liveRooms"):
    db_ref = db.reference(collection)
    doc_ref = db_ref.child(name).get()
    if doc_ref: #exists
        db_ref.child(name).set([])


def download_data_list(name, key, collection="liveRooms"):
    db_ref = db.reference(collection)
    doc_ref = db_ref.child(name).get()
    if doc_ref: #exists
        db_ref.child(name).child(key).get().values()

def get_all_data_keys(collection="liveRooms"):
    db_ref = db.reference(collection)
    return [*db_ref.get(False, True)] #get keys as list



def clear_documents(collection, deadline):
    ref = db.reference(collection)
    docs = ref.get()
    if not docs:
        return
    for doc in docs.keys():
        doc_data = docs[doc]
        time_c = doc_data["time_created"]
        #)
        if time.time()-float(time_c) >= deadline:
            delete_data(doc, collection)
            print(f"Deleted Temporary File: {doc} after {time.time()-float(time_c)} seconds of existence, more than the deadline of {deadline}.")

def get_number_of_documents(collection, is_list=True):
    docs = db.reference(collection).get()
    if not docs:
        return 0
    if is_list:
        count_query = len(docs)
    else:
        count_query=len(docs.keys())
    return count_query

def search_documents(collection, query, user="", is_list=True):
    db_ref = db.reference(collection)
    docs = db_ref.get()
    if not docs:
        return {}
    result = []
    duplicates = []
    if is_list:
        _iter = range(len(docs))
    else:
        _iter = docs.keys()
    for doc in _iter:
        doc_data = docs[doc]
        quiz_name = doc_data["quiz_name"]
        if ((user=="") or (user == doc_data["user"]["uid"])) and ("quiz_data" in doc_data):
            closeness = fuzz.ratio(quiz_name, query)
            if closeness in duplicates:
                closeness -= random.uniform(0.01, 0.02)
            duplicates.append(closeness)
            result.append({
                "closeness": closeness,
                "id": doc,
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



def get_all_documents(collection, user="", is_list=True):
    db_ref = db.reference(collection)
    docs = db_ref.get()
    result = []
    i = 0
    if not docs:
        return {}
    
    if is_list:
        _iter = range(len(docs))
    else:
        _iter = docs.keys()
    for doc in _iter:
        doc_data = docs[doc]
        quiz_name = doc_data["quiz_name"]
        if ((user=="") or (user==doc_data["user"]["uid"])) and ("quiz_data" in doc_data):
            result.append({
                "closeness": i,
                "id": doc,
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