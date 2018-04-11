"""Following example works with Python Client"""
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory

"""Create a connection, get store, insert new document into store"""
# create a connection using path:user@password
connection = ConnectionFactory.get_connection(url="localhost:5678")

# Get a store and assign it as a DocumentStore object
store = connection.get_store(store_path="/sample_store1")

# Json string or json dictionary
json_dict = {"_id": "id004",
             "name": "Tom",
             "age": 36,
             "address": {
                 "street": "13 Shadow Av",
                 "city": "Tahoe"}
             }

# Create new document from json_document
new_document = connection.new_document(dictionary=json_dict)
print(new_document.as_json_str())
# Insert json dictionary into the store
store.insert_or_replace(json_dictionary=json_dict)

delete = connection.delete_store(store_path='/sample_store1')

# close
connection.close()
