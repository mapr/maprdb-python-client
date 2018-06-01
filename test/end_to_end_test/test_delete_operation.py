#!/usr/bin/env python
from __future__ import unicode_literals

from ojai.types.OTime import OTime
from ojai.types.OTimestamp import OTimestamp

from mapr.ojai.ojai.OJAIDocument import OJAIDocument
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class DeleteTest(unittest.TestCase):
    url = "192.168.33.11:5678?auth=basic;user=root;password=r00t;" \
          "ssl=true;" \
          "sslCA=/opt/mapr/conf/ssl_truststore.pem;" \
          "sslTargetNameOverride=node1.cluster.com"

    dict_stream = [{'_id': "id01", 'test_int': 51, 'test_str': 'strstr'},
                   {'_id': 'id02', 'mystr': 'str', 'test_int': 51, 'test_str': 'strstr'},
                   {'_id': 'id03', 'test_int': 51, 'test_otime': OTime(timestamp=1518689532), 'test_str': 'strstr'},
                   {'_id': 'id04', 'test_int': 51, 'test_timestamp': OTimestamp(millis_since_epoch=29877132000),
                    'test_str': 'strstr'},
                   {'_id': 'id05', 'test_int': 51, 'test_bool': True, 'test_str': 'strstr'},
                   {'_id': 'id06', 'test_int': 51, 'test_str': 'strstr'},
                   {'_id': 'id07', 'test_int': 51, 'test_str': 'strstr'},
                   {'_id': 'id08', 'test_int': 51, 'test_str': 'strstr', 'test_dict': {'test_int': 5}},
                   {'_id': 'id09', 'test_int': 51, 'test_str': 'strstr', 'test_list': [5, 6]},
                   {'_id': 'id10', 'test_int': 51, 'test_str': 'strstr', 'test_null': None}]

    def test_delete_document(self):
        connection = ConnectionFactory.get_connection(connection_str=DeleteTest.url)

        if connection.is_store_exists(store_path='/delete-test-store1'):
            document_store = connection.get_store(store_path='/delete-test-store1')
        else:
            document_store = connection.create_store(store_path='/delete-test-store1')

        document = None

        for doc in DeleteTest.dict_stream:
            document = connection.new_document(dictionary=doc)
            document_store.insert_or_replace(doc=document)

        document_store.delete(doc=document)
        self.assertEqual(document_store.find_by_id('id10'), {})

    def test_delete_id(self):
        connection = ConnectionFactory.get_connection(connection_str=DeleteTest.url)

        if connection.is_store_exists(store_path='/delete-test-store1'):
            document_store = connection.get_store(store_path='/delete-test-store1')
        else:
            document_store = connection.create_store(store_path='/delete-test-store1')

        document_store.delete(_id='id09')

        self.assertEqual(document_store.find_by_id('id09'), {})

    def test_delete_document_stream(self):
        connection = ConnectionFactory.get_connection(connection_str=DeleteTest.url)

        if connection.is_store_exists(store_path='/delete-test-store1'):
            document_store = connection.get_store(store_path='/delete-test-store1')
        else:
            document_store = connection.create_store(store_path='/delete-test-store1')

        doc_stream = []

        for i in range(1, 5):
            doc_stream.append(OJAIDocument().from_dict(DeleteTest.dict_stream[i]))

        document_store.delete(doc_stream=doc_stream)


if __name__ == '__main__':
    test_classes_to_run = [DeleteTest]
    loader = unittest.TestLoader()
    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
