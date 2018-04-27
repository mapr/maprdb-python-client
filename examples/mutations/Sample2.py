"""Following example works with Python Client"""
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory
"""Sample for increment operation"""

# create a connection
connection = ConnectionFactory.get_connection(url="localhost:5678")

# Get a store and assign it as a DocumentStore object
if connection.is_store_exists(store_path='/update_store1'):
    document_store = connection.get_store(store_path='/update_store1')
else:
    document_store = connection.create_store(store_path='/update_store1')

# Create new mutation
doc_mutation = connection.new_mutation().increment('age', 4)

# Execute increment
document_store.increment('user0001', 'age', 4)

# Execute increment as mutation
document_store.update('user0001', doc_mutation)

document = document_store.find_by_id('user0001')

print(document)
