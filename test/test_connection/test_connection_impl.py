#!/usr/bin/env python
from __future__ import unicode_literals

import grpc

from mapr.ojai.proto.gen.maprdb_server_pb2 import CreateTableRequest, TableExistsRequest, ErrorCode
from mapr.ojai.proto.gen.maprdb_server_pb2_grpc import MapRDbServerStub
from mapr.ojai.storage.ConnectionImpl import ConnectionImpl
from mapr.ojai.storage.ConnectionManagerImpl import ConnectionManagerImpl
from mapr.ojai.storage.connection_constants import DRIVER_BASE_URL, SERVICE_PORT

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class ConnectionTest(unittest.TestCase):

    def test_connection(self):
        # TODO doesn't work
        # url = str(DRIVER_BASE_URL) + 'localhost:' + str(SERVICE_PORT)
        url = 'localhost:5678'
        connection = ConnectionImpl(connection_url=url)
        before_create = connection.is_table_exists(table_path='/test-store1')
        self.assertFalse(before_create)
        response = connection.create_table(table_path='/test-store1')
        self.assertTrue(response)
        after_create = connection.is_table_exists(table_path='/test-store1')
        self.assertTrue(after_create)
        response_two = connection.create_table(table_path='/test-store1')
        self.assertFalse(response_two)
        delete_response = connection.delete_table(table_path='/test-store1')
        self.assertTrue(delete_response)

    def test_get_store(self):
        doc_dict = {'_id': 15, 'test_int': 51, 'test_str': 'strstr'}
        url = 'localhost:5678'
        connection = ConnectionImpl(connection_url=url)
        before_create = connection.is_table_exists(table_path='/test-store2')
        # self.assertFalse(before_create)
        self.assertTrue(before_create)
        # response = connection.create_table(table_path='/test-store2')
        # self.assertTrue(response)
        document_store = connection.get_store(store_name='/test-store2')
        document = connection.new_document(dictionary=doc_dict)
        document_store.insert_or_replace(doc=document)



if __name__ == '__main__':
    test_classes_to_run = [ConnectionTest]
    loader = unittest.TestLoader()
    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
