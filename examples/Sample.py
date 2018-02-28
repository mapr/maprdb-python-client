"""Following example works with Python Client"""
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory

"""Create a connection, get store, insert new document into store"""
# create a connection using path:user@password
connection = ConnectionFactory.get_connection(url="hostname:port:user@password")

# Get a store and assign it as a DocumentStore object
store = connection.create_store(store_name="/test_name")

# Json string or json dictionary
json_dict = {"name": "Joe",
             "age": 50,
             "address": {
                 "street": "555 Moon Way",
                 "city": "Gotham"}
             }

# Create new document from json_document
new_document = connection.new_document(json_dict)

# Insert new document into the store
store.insert_or_replace(new_document)

# close
connection.close()
