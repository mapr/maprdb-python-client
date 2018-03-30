#!/usr/bin/env python
from __future__ import unicode_literals

import grpc

from ojai.o_types.ODate import ODate
from ojai.o_types.OTime import OTime
from ojai.o_types.OTimestamp import OTimestamp
from mapr.ojai.ojai.OJAIDocument import OJAIDocument
from mapr.ojai.ojai.OJAIDocumentStore import OJAIDocumentStore
from mapr.ojai.proto.gen.maprdb_server_pb2 import CreateTableRequest, TableExistsRequest, ErrorCode
from mapr.ojai.proto.gen.maprdb_server_pb2_grpc import MapRDbServerStub
from mapr.ojai.storage.OJAIConnection import OJAIConnection
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory
from mapr.ojai.storage.connection_constants import DRIVER_BASE_URL, SERVICE_PORT

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class FindTest(unittest.TestCase):

    def test_find_by_id(self):
        url = 'localhost:5678'
        connection = ConnectionFactory.get_connection(url=url)

        if connection.is_store_exists(store_path='/find-test-store1'):
            document_store = connection.get_store(store_path='/find-test-store1')
        else:
            document_store = connection.create_store(store_path='/find-test-store1')
        document = connection.new_document(dictionary={'_id': 'id008',
                                                       'test_int': 51,
                                                       'test_str': 'strstr',
                                                       'test_dict': {'test_int': 5},
                                                       'test_list': [5, 6],
                                                       'test_null': None,
                                                       'test_otime': OTime(timestamp=1518689532)})

        document_store.insert_or_replace(doc=document)

        self.assertTrue(connection.is_store_exists('/find-test-store1'))
        doc = document_store.find_by_id('id008', as_object=True)

        self.assertEqual(doc.as_dictionary(), document.as_dictionary())

    def test_insert_find_large_doc(self):
        document = OJAIDocument().set_id("121212") \
            .set('test_int', 123) \
            .set('first.test_int', 1235) \
            .set('first.test_long', 123456789) \
            .set('first.test_time', OTime(timestamp=1518689532)) \
            .set('first.test_date', ODate(days_since_epoch=3456)) \
            .set('first.test_bool', True) \
            .set('first.test_bool_false', False) \
            .set('first.test_invalid', ODate(days_since_epoch=3457)) \
            .set('first.test_str', 'strstr') \
            .set('first.test_dict', {'a': 1, 'b': 2}) \
            .set('first.test_dict2', {}) \
            .set('first.test_list', [1, 2, 'str', False, ODate(days_since_epoch=3457)]) \

        url = 'localhost:5678'
        connection = ConnectionFactory.get_connection(url=url)

        if connection.is_store_exists(store_path='/find-test-store1'):
            document_store = connection.get_store(store_path='/find-test-store1')
        else:
            document_store = connection.create_store(store_path='/find-test-store1')

        document_store.insert_or_replace(doc=document)

        self.assertTrue(connection.is_store_exists('/find-test-store1'))
        doc = document_store.find_by_id('121212', as_object=True)

        self.assertEqual(doc.as_dictionary(), document.as_dictionary())

    def test_find_by_id_as_dict(self):
        url = 'localhost:5678'
        connection = ConnectionFactory.get_connection(url=url)

        if connection.is_store_exists(store_path='/find-test-store1'):
            document_store = connection.get_store(store_path='/find-test-store1')
        else:
            document_store = connection.create_store(store_path='/find-test-store1')

        self.assertTrue(connection.is_store_exists('/find-test-store1'))
        doc = document_store.find_by_id('121212')

        document = OJAIDocument().set_id("121212") \
            .set('test_int', 123) \
            .set('first.test_int', 1235) \
            .set('first.test_long', 123456789) \
            .set('first.test_time', OTime(timestamp=1518689532)) \
            .set('first.test_date', ODate(days_since_epoch=3456)) \
            .set('first.test_bool', True) \
            .set('first.test_bool_false', False) \
            .set('first.test_invalid', ODate(days_since_epoch=3457)) \
            .set('first.test_str', 'strstr') \
            .set('first.test_dict', {'a': 1, 'b': 2}) \
            .set('first.test_dict2', {}) \
            .set('first.test_list', [1, 2, 'str', False, ODate(days_since_epoch=3457)])

        self.assertEqual(doc, document.as_dictionary())


if __name__ == '__main__':

    test_classes_to_run = [FindTest]
    loader = unittest.TestLoader()
    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
