"""Following example works with Python Client"""
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory

"""Create a connection, get store, insert new document into store"""
# create a connection using path:user@password
connection_string = "localhost:5678?auth=basic;user=mapr;password=mapr;" \
          "ssl=true;" \
          "sslCA=/opt/mapr/conf/ssl_truststore.pem;" \
          "sslTargetNameOverride=node.mapr.com"
connection = ConnectionFactory.get_connection(connection_str=connection_string)

# Get a store and assign it as a DocumentStore object
store = connection.create_store(store_path="/sample_store1")

# Json string or json dictionary
json_dict = {"_id": "id001",
             "name": "Joe",
             "age": 50,
             "address": {
                 "street": "555 Moon Way",
                 "city": "Gotham"}
             }

# Create new document from json_document
new_document = connection.new_document(dictionary=json_dict)
print(new_document.as_json_str())
# Insert new document into the store
store.insert_or_replace(doc=new_document)

# close
connection.close()
