"""Following example works with Python Client"""
from mapr.ojai.ojai_query.OJAIQuery import OJAIQuery
from mapr.ojai.ojai_query.OJAIQueryCondition import OJAIQueryCondition
from mapr.ojai.ojai_query.QueryOp import QueryOp
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory

"""Create a connection, get store, insert new document into store"""
# create a connection
connection = ConnectionFactory.get_connection(url="localhost:5678")

# Get a store and assign it as a DocumentStore object
if connection.is_store_exists(store_path='/find_sample_store1'):
    document_store = connection.get_store(store_path='/find_sample_store1')
else:
    document_store = connection.create_store(store_path='/find_sample_store1')

query_condition = OJAIQueryCondition()\
    .or_()\
    .is_('address.street', QueryOp.EQUAL, '351 Hoger Way')\
    .is_('address.street', QueryOp.EQUAL, '39 De Mattei Court')\
    .is_('address.zipCode', QueryOp.EQUAL, 99999).close().close().build()

query = OJAIQuery().select(['address']).where(query_condition).build()

doc_stream = document_store.find(query, results_as_document=True, include_query_plan=True).iterator()

for doc in doc_stream:
    print(doc.as_dictionary())
