"""Following example works with Python Client"""
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory

"""Create a connection, get store, insert new document into store"""
# create a connection using path:user@password
connection = ConnectionFactory.get_connection(connection_str="localhost:5678")

# Get a store and assign it as a DocumentStore object
store = connection.get_store(store_path="/sample_store1")

# Json string or json dictionary
json_dict = {"_id": "id001",
             "name": "Jim",
             "age": 30,
             "address": {
                 "street": "621 Moon Way",
                 "city": "NY"}
             }

# Create new document from json_document
new_document = connection.new_document(dictionary=json_dict)
# Insert document into the store where a document with the same _id already presents
store.insert(doc=new_document)

# close
connection.close()
