"""Following example works with Python Client"""
from ojai.o_types.ODate import ODate
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory

"""Create a connection, get store, insert new document into store"""
# create a connection using path:user@password
connection = ConnectionFactory.get_connection(url="localhost:5678")

# Get a store and assign it as a DocumentStore object
store = connection.get_store(store_path="/sample_store1")

# Json string or json dictionary
json_dict = {"_id": "id002",
             "name": "Joe",
             "age": 50,
             "address": {
                 "street": "555 Moon Way",
                 "city": "Gotham"}
             }

# Json string or json dictionary
payment = {"payment_method": "card",
           "name": "visa",
           "card_info": {
               "number": "1234 1234 1234 1234",
               "exp_date": ODate.parse("2022-10-24"),
               "cvv": 123}
           }

# Create new document from json_document
new_document = connection.new_document(dictionary=json_dict)
# Add nested dictionary into document
new_document.set(field_path='payment', value=payment)
# Insert or replace new document into the store
store.insert_or_replace(doc=new_document)

# close
connection.close()
