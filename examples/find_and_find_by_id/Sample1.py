"""Following example works with Python Client"""
from mapr.ojai.ojai_query.QueryOp import QueryOp
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory

"""Create a connection, get store, insert new documents into store, find document by id"""
# create a connection
connection_string = "localhost:5678?auth=basic;user=mapr;password=mapr;" \
          "ssl=true;" \
          "sslCA=/opt/mapr/conf/ssl_truststore.pem;" \
          "sslTargetNameOverride=node.mapr.com"
connection = ConnectionFactory.get_connection(connection_str=connection_string)

# Get a store and assign it as a DocumentStore object
if connection.is_store_exists(store_path='/find_sample_store1'):
    document_store = connection.get_store(store_path='/find_sample_store1')
else:
    document_store = connection.create_store(store_path='/find_sample_store1')

# Json string or json dictionary
document_list = [{'_id': 'user0000', 'age': 35, 'firstName': 'John', 'lastName': 'Doe', 'address':
    {'street': '350 Hoger Way', 'city': 'San Jose', 'state': 'CA', 'zipCode': 95134},
                  'phoneNumbers': [{'areaCode': 555, 'number': 5555555}, {'areaCode': '555', 'number': '555-5556'}]},
                 {'_id': 'user0001', 'age': 26, 'firstName': 'Jane', 'lastName': 'Dupont',
                  'address': {'street': '320 Blossom Hill Road', 'city': 'San Jose', 'state': 'CA', 'zipCode': 95196},
                  'phoneNumbers': [{'areaCode': 555, 'number': 5553827}, {'areaCode': '555', 'number': '555-6289'}]},
                 {'_id': 'user0002', 'age': 45, 'firstName': 'Simon', 'lastName': 'Davis',
                  'address': {'street': '38 De Mattei Court', 'city': 'San Jose', 'state': 'CA', 'zipCode': 95142},
                  'phoneNumbers': [{'areaCode': 555, 'number': 5425639}, {'areaCode': '555', 'number': '542-5656'}]}]

# Insert new document into the store
document_store.insert_or_replace(doc_stream=document_list)

# Find document by _id field
document = document_store.find_by_id('user0001', condition=connection.new_condition().or_() \
                                     .is_('address.street', QueryOp.EQUAL, '320 Blossom Hill Road') \
                                     .is_('address.zipCode', QueryOp.EQUAL, 95134).close().close().build(),
                                     field_paths=["age", "firstName"], timeout=5)

# Print the document
print(document)

# close
connection.close()
