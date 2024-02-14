
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
    """
    This function connects the user to firebase and authenticates 
    the connection using the certificate JSON file.

    :param cert_name: the name of the certificate JSON file
    :return: the firestore client
    """
    
    cred = credentials.Certificate(cert_name)
    app = firebase_admin.initialize_app(cred)
    client = firestore.client()
    return client

#selecting the database collection
def retrieve_reference(client, collection_name):
    """
    This function gets a reference to the collection specified by collection_name.

    :param client: the firestore client
    :param collection_name: the name of the collection
    :return: a reference to the collection
    """

    ref = client.collection(collection_name)
    return ref

# set an element in the database
def set_collection_element(ref, element):
    """
    This function is used to modify elements in the firestore collection.

    :param ref: the reference to the collection
    """
    ref.document(str(element.uuid)).set(
        element.to_dict()
    )

# printing it all out
def print_collection(ref):
    """
    This function prints out the stream of the reference variable. This is useful for 
    making sure that data was correctly uploaded to firebase.

    :param ref: the reference to the collection
    """
    docs = ref.stream()
    for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")

# perform a single query the database
def query_database(ref, retrievals, field=None, operator=None, value=None):
    """
    This function executes a query on the database and returns the stream of the 
    query by specifying the variables to retrieve and optionally the field, operator, and 
    value necessary for a conditional retrieval.

    :param ref: the reference to the collection
    :param retrievals: the variables to retrieve
    :param field: (optional) the field to compare
    :param operator: (optional) the comparison operator
    :param value: (optional) the value to compare the field to
    :return: the stream of the query
    """
    if field is not None and operator is not None and value is not None:
        query = ref.where(field, operator, value=value)
    else:
        query = ref
    query = query.select(retrievals)
    results = query.stream()
    return results

# client = verify_connection('warm-up-project-3050.json')
# ref = retrieve_reference(client, "3050-Dealership")
# # print_collection(ref)
# query_database(ref, ['make', 'model', 'mpg'], 'mpg', '>=', 25)
