"""Following example works with Python Client"""
from mapr.ojai.ojai_query.QueryOp import QueryOp
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory

"""Create a connection, get store, insert new document into store"""
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

query_condition = connection.new_condition() \
    .or_() \
    .is_('address.street', QueryOp.EQUAL, '350 Hoger Way') \
    .is_('address.street', QueryOp.EQUAL, '38 De Mattei Court') \
    .is_('address.zipCode', QueryOp.EQUAL, 95196).close().close().build()

query = connection.new_query().select(['address.street', 'address.zipCode'])\
    .where(query_condition).build().query_dict()

options = {
    'ojai.mapr.query.timeout-milliseconds': 1000,
}
query_result = document_store.find(query, options=options)

for doc in query_result:
    print(doc)
