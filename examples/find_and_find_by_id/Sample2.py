"""Following example works with Python Client"""
from mapr.ojai.ojai_query.QueryOp import QueryOp
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory

"""Create a connection, get store, find document in store"""
# create a connection
connection = ConnectionFactory.get_connection(url="localhost:5678")

# Get a store and assign it as a DocumentStore object
if connection.is_store_exists(store_path='/find_sample_store1'):
    document_store = connection.get_store(store_path='/find_sample_store1')
else:
    document_store = connection.create_store(store_path='/find_sample_store1')

print("Create find request with query as a dictionary.")
query_result = document_store.find(
    {'$select': ['*'], '$where': {'$and': [{'$ge': {u'age': 26}}, {'$le': {u'age': 35}}]}},
    include_query_plan=False, results_as_document=False)

print(query_result.get_query_plan())
for d in query_result.iterator():
    print(d)

print("Create find request with query as a OJAIQuery object")
query = connection.new_query().select(['*']).where(connection.new_condition().and_().is_('age', QueryOp.GREATER_OR_EQUAL, 26)
                                        .is_('age', QueryOp.LESS_OR_EQUAL, 35).close().close().build()).build()
query_result = document_store.find(query, include_query_plan=True, results_as_document=False, timeout=1)
print(query_result.get_query_plan())
for d in query_result.iterator():
    print(d)
