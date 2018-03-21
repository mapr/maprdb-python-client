"""Following example works with Python Client.
Inserting document with multiple field and nested document, array, dict"""
from ojai.o_types.ODate import ODate
from ojai.o_types.OTime import OTime
from ojai.o_types.OTimestamp import OTimestamp
from mapr.ojai.ojai.OJAIDocument import OJAIDocument
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

byte_array = bytearray([0x13, 0x00, 0x00, 0x00, 0x08, 0x00])
doc = OJAIDocument().set_id("id003") \
            .set('test_int', 14) \
            .set('first.test_int', 1235) \
            .set('first.test_long', 123456789) \
            .set('first.test_time', OTime(timestamp=1518689532)) \
            .set('first.test_timestamp', OTimestamp(millis_since_epoch=29877132000)) \
            .set('first.test_date', ODate(days_since_epoch=3456)) \
            .set('first.test_bool', True) \
            .set('first.test_bool_false', False) \
            .set('first.test_invalid', ODate(days_since_epoch=3457)) \
            .set('first.test_str', 'strstr') \
            .set('first.test_dict', {'a': 1, 'b': 2}) \
            .set('first.test_dict2', {}) \
            .set('first.test_list', [1, 2, 'str', False, ODate(days_since_epoch=3457)]) \
            .set('first.test_binary', byte_array)

# Create new document from json_document
new_document = connection.new_document(dictionary=json_dict)
doc.set('first.second.nested_doc', new_document)
# Insert new document into the store
store.insert_or_replace(doc=doc)

# close
connection.close()
