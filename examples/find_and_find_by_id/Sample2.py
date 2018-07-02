"""Following example works with Python Client"""
from mapr.ojai.ojai_query.QueryOp import QueryOp
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory

"""Create a connection, get store, find document in store"""
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

options = {
    'ojai.mapr.query.include-query-plan': True,
    'ojai.mapr.query.timeout-milliseconds': 1000,
    'ojai.mapr.query.result-as-document': False
    }
query_dict = {'$select': ['*'],
              '$where': {'$and': [
                  {'$ge': {u'age': 26}},
                  {'$le': {u'age': 35}}]}}

print("Create find request with query as a dictionary.")
query_result = document_store.find(
    query_dict,
    options=options)

print(query_result.get_query_plan())
for d in query_result:
    print(d)

print("Create find request with query as a OJAIQuery object")
query = connection.new_query().select(['*']) \
    .where(connection.new_condition().and_().is_('age', QueryOp.GREATER_OR_EQUAL, 26)
           .is_('age', QueryOp.LESS_OR_EQUAL, 35).close().close().build()).build()

query_result = document_store.find(query, options=options)
print(query_result.get_query_plan())

for d in query_result:
    print(d)
