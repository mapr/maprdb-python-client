"""Following example works with Python Client"""
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory

"""Create a connection, get store, insert new document into store"""
# create a connection using path:user@password
connection = ConnectionFactory.get_connection(url="localhost:5678")

# Get a store and assign it as a DocumentStore object
document_store = connection.create_store(store_path="/update_store1")
"""Sample for update operation."""
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

# Create doc mutation
doc_mutation = connection.new_mutation()\
    .set_or_replace('mutation_field', 50)\
    .append('phoneNumbers', [{'areaCode': 111, 'number': 9369992}])\
    .merge('address', {'country': 'USA'})

document_store.update('user0002', doc_mutation)

document = document_store.find_by_id('user0002')

print(document)
