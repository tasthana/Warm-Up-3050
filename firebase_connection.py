
# firebase connection file 

#imports 
from firebase_admin import db
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#credentials and verification 
cred = credentials.Certificate('warm-up-project-3050.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

#selecting the database collection
users_ref = db.collection("3050-Dealership")
docs = users_ref.stream()

#printing it all out.= 
for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")
