"""Following example works with Python Client"""
from mapr.ojai.ojai_query.OJAIQuery import OJAIQuery
from mapr.ojai.ojai_query.OJAIQueryCondition import OJAIQueryCondition
from mapr.ojai.ojai_query.QueryOp import QueryOp
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory

"""Create a connection, get store, insert new document into store"""
# create a connection using path:user@password
connection = ConnectionFactory.get_connection(url="localhost:5678")

# Get a store and assign it as a DocumentStore object
if connection.is_store_exists(store_path='/find_sample_store1'):
    document_store = connection.get_store(store_path='/find_sample_store1')
else:
    document_store = connection.create_store(store_path='/find_sample_store1')

query = OJAIQuery().select(['address']).where(OJAIQueryCondition().and_().is_('age', QueryOp.GREATER_OR_EQUAL, 26)
                                              .is_('age', QueryOp.LESS_OR_EQUAL, 35).close().close().build()).build()

doc_stream = document_store.find(query).iterator()

print(doc_stream)
