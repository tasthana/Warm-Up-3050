# Import database module.
from firebase_admin import db
import firebase_admin
from firebase_admin import credentials

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('warm-up-project-3050.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

users_ref = db.collection("3050-Dealership")
docs = users_ref.stream()

for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")
