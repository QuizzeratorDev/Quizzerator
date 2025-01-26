import api.firebase_db as firebase_db

def clear():
    firebase_db.clear_documents("tempCollection", 80000)