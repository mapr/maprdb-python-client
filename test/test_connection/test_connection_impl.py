#!/usr/bin/env python
from __future__ import unicode_literals

import grpc

from mapr.ojai.o_types.OInterval import OInterval
from mapr.ojai.o_types.OTime import OTime
from mapr.ojai.o_types.OTimestamp import OTimestamp
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

    def test_get_store_and_insert(self):
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
        # doc_dict = {'_id': "15", 'test_int': 51, 'test_str': 'strstr'}
        url = 'localhost:5678'
        connection = ConnectionImpl(connection_url=url)

        delete_response = connection.delete_table(table_path='/test-store5')
        self.assertTrue(delete_response)
        before_create = connection.is_table_exists(table_path='/test-store5')
        self.assertFalse(before_create)
        # self.assertTrue(before_create)
        response = connection.create_table(table_path='/test-store5')
        self.assertTrue(response)
        document_store = connection.get_store(store_name='/test-store5')
        for doc in dict_stream:
            document = connection.new_document(dictionary=doc)
            print('Insert document with ID: ' + str(document.get_id()))
            res = document_store.insert_or_replace(doc=document)
            self.assertEqual(res, 0, msg='Document insertiong with id: ' + str(document.get_id())
                                         + ' failed. Error code: ' + str(res))

    def test_find_by_id(self):
        url = 'localhost:5678'
        connection = ConnectionImpl(connection_url=url)

        # delete_response = connection.delete_table(table_path='/test-store6')
        # self.assertTrue(delete_response)
        before_create = connection.is_table_exists(table_path='/test-store6')
        # self.assertFalse(before_create)
        self.assertTrue(before_create)
        # response = connection.create_table(table_path='/test-store6')
        # self.assertTrue(response)
        document_store = connection.get_store(store_name='/test-store6')
        doc = document_store.find_by_id(_id='id06')


if __name__ == '__main__':

    error_code = {0: 'NO_ERROR',
                  1: 'UNKNOWN_PAYLOAD_ENCODING',
                  2: 'CLUSTER_NOT_FOUND',
                  3: 'PATH_NOT_FOUND',
                  4: 'TABLE_NOT_FOUND',
                  5: 'ENCODING_ERROR',
                  6: 'DECODING_ERROR'}

    for k, v in error_code.iteritems():
        print(str(k) + " : " + str(v))

    test_classes_to_run = [ConnectionTest]
    loader = unittest.TestLoader()
    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
