import firebase_db

def clear():
    firebase_db.clear_documents("tempCollection", 10)