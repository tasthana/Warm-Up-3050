
# firebase connection file 

#imports 
from firebase_admin import db
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from car import Car



#credentials and verification 
def verify_connection(cert_name):
    #cred = credentials.Certificate('warm-up-project-3050.json')
    cred = credentials.Certificate(cert_name)
    app = firebase_admin.initialize_app(cred)
    client = firestore.client()
    return client

#selecting the database collection
def retrieve_reference(client, collection_name):
    #ref = db.collection("3050-Dealership")
    ref = client.collection(collection_name)
    return ref

# set an element in the database
def set_collection_element(ref, element):
    ref.document(element.uuid).set(
        element.to_dict()
    )

# printing it all out
def print_collection(ref):
    docs = ref.stream()
    for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")

# perform a single query the database
def query_database(ref, retrievals, field, operator, value):
    query = ref.where(filter=FieldFilter(field, operator, value=value))
    query = query.select(retrievals)
    results = query.stream()
    return results



# client = verify_connection('warm-up-project-3050.json')
# ref = retrieve_reference(client, "3050-Dealership")
# # print_collection(ref)
# query_database(ref, ['make', 'model', 'mpg'], 'mpg', '>=', 25)