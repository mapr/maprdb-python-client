"""Following example works with Python Client"""
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory

"""Create a connection, get store, insert new document into store"""
# create a connection using path:user@password
connection = ConnectionFactory.get_connection(connection_str="localhost:5678")

# Get a store and assign it as a DocumentStore object
store = connection.get_store(store_path="/sample_store1")

# Json string or json dictionary
json_dict = {"_id": "id001",
             "name": "Donald",
             "age": 71,
             "address": {
                 "street": "1600 Pennsylvania Ave",
                 "city": "Washington DC"}
             }

# Create new document from json_document
new_document = connection.new_document(dictionary=json_dict)
# replace document into the store
store.replace(doc=new_document)

# close
connection.close()
