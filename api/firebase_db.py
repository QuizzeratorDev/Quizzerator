import firebase_admin, time
from firebase_admin import credentials
from firebase_admin import firestore, json
from flask import jsonify
from rapidfuzz import fuzz

import os,json

db = 0
def setup():
    
    #cred_dict = json.loads(os.environ.get('FIREBASE_CREDENTIALS'))
    cred_dict = {
    "type": "service_account",
    "project_id": "quizzerator",
    "private_key_id": "86c8037ecaa5cb2cf457b35ede03ce376dde4975",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDW9HFX2XRjU+kD\ntJmyNP4DlzEDq0x+1DNEvbS5szrfYlv9ZbMtbeUQ0MDs3g2lmdj7pChS2QNUUFHG\nWZqzGB0Tzx6H6smco5GXUvMag/AmRzW3kQh3pkncXzVTPCHcmgtwiKp4vVkFxK8k\nYagx0fvVCRW4kb+HvWO7RCq1Us4sw/K5s3mt6wuKVNbFo1XdhTRXkQgfwu0Fl4Y3\nsnaWnzQQ0oP0N5O4gTTYTeqJ8AkI9RahzxLb7E3sl/XMUCpMoP9PN60T6mIo9Dn6\noDOj0tvffuYNBUq1Hi9bu7Mac40N1kPlXHZEXBfsk6tduPdECigr2ozsWsUHn0sY\nH3eFzTaZAgMBAAECggEASuymSzw5RNv9JvT+865j8eVzyLcfMUAO5MGJKodOGIoE\nzXTy+P1KsEtLS+T0dcoD52anRYVuEyfx8QTPluhrTjnOBwswHiCngUsBALeHcBg3\nIZZ0kJwON7mZ8TrPBMFPBnkkjnRVgNy3PaOqiD8MnAuQHibzT0GU7zPJ/SzxP4mj\n17ojHUHvR7jJHZJqdwLCrmoO3p+i8LOEReCdAjBUBv5rnVdEF5dIKadTjpz++ZTt\n5kEuw8pzcxLsdPdAMGiGt2eE7eifsOrJGp3KP7LJMMgPRH2reoc98lCi8lvQjfEB\nG7KyJ42pNJXd/C7H4Jb2aAMay7+gWjW8cLIaI/hgXwKBgQDtql/MjjoK8q1RtT7E\n+73AnAlFzPey//ORxvAS6p5bE5JvhiWVqvty2yWJ4Gq0+2X6INN9XD4sTvfIx286\nawDdDZjT2PHgx9bV0JKN534ofyfxGuuwD3Ej7n+kbE4pEVQxuWZgc0R6KY6qsb3K\n/tiAmswoiFW2+FZ4NhUB9EklKwKBgQDniY72IBa1TGrjR7939YdDfFxymNR6IEjq\n555mfKsHrDcf25yE3vLrVjHq78T0DMxM0cVWeP40vVpuQSJ7tJbKqPdIS4ibAMP7\n67YxIVSshc5ylVTtUoI2hAoORuEMLGkRfGCHK20DkPJ+dfHy+697ufGWZvZeD3w1\n2ZoL+mp5SwKBgHmrolWnbmGScVaGMjdIJZGIkFqynxB9ZiV4MgmNITrBH1OG2pDv\nssDPHj2irR4wIbnWuk7QPWgTmVipePDwPMXuIxI5W0LXK83UdGK/Y1+6ESmmvYgp\nr6NUgvYbGDyACZlXL+kquaDMy6PpUJ+urgnQtbn+ads88Y+jKEgS1qt3AoGBAOJn\nbFfXwNy/QLXF7sAKYp3m+S9Fql9ROnwYyJdGyKbUC4MnZ8G1kKv2uREWK+zIpu1n\nIiQQY+KGVesB3gpA6EJ7PnJ/CbEn6nxoXNtl0DpzDRCWXVlDGPjd3Edhn6YbtxHW\nIT2LhSm7jqOCCXikC1Bc3pNHUxle4wJ1KWEVGRBJAoGBAJssogj7Is4KBvL8u5BV\nz8K/U+l0DdcJTsqHDRShvz8ZU+yjhvwDdkFiadeTQomXCoIaE05gH/iBqsMMdPI2\nsyZ9eme0/yTkoulM86Itn1Gle3R5W2sgXpkBrFdmoLTLs494JCB21FIhO3f0ywBa\nV/LLc76rHCkTa+ARQMy0j3YD\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-60izn@quizzerator.iam.gserviceaccount.com",
    "client_id": "102702821627635685921",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-60izn%40quizzerator.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
    }


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
    for doc in docs:
        doc_data = doc.to_dict()
        quiz_name = doc_data["quiz_name"]
        closeness = fuzz.ratio(quiz_name, query)
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