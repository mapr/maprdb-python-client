#!/usr/bin/env python
from __future__ import unicode_literals

from mapr.ojai.exceptions.StoreNotFoundError import StoreNotFoundError
from mapr.ojai.ojai_query.OJAIQuery import OJAIQuery
from mapr.ojai.ojai_query.OJAIQueryCondition import OJAIQueryCondition
from mapr.ojai.ojai_query.QueryOp import QueryOp
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class FindTest(unittest.TestCase):
    url = "192.168.33.11:5678?auth=basic;user=root;password=r00t;" \
          "ssl=true;" \
          "sslCA=/opt/mapr/conf/ssl_truststore.pem;" \
          "sslTargetNameOverride=node1.cluster.com"

    def test_simple_find(self):
        connection = ConnectionFactory.get_connection(connection_str=FindTest.url)

        if connection.is_store_exists(store_path='/find-test-store1'):
            document_store = connection.get_store(store_path='/find-test-store1')
        else:
            document_store = connection.create_store(store_path='/find-test-store1')
        document = connection.new_document(dictionary={'_id': 'id008',
                                                       'test_int': 51,
                                                       'test_str': 'strstr',
                                                       'test_dict': {'test_int': 5},
                                                       'test_list': [5, 6],
                                                       'test_null': None})

        document_store.insert_or_replace(doc=document)

        query = OJAIQuery().select(['_id', 'test_int', 'test_str', 'test_dict', 'test_list', 'test_null']).build()

        self.assertTrue(connection.is_store_exists('/find-test-store1'))
        doc_stream = document_store.find(query)
        for doc in doc_stream:
            self.assertEqual(doc, document.as_dictionary())

    def test_find_on_empty_table(self):
        connection = ConnectionFactory.get_connection(connection_str=FindTest.url)

        if connection.is_store_exists(store_path='/find-test-store2'):
            document_store = connection.get_store(store_path='/find-test-store2')
        else:
            document_store = connection.create_store(store_path='/find-test-store2')

        query = OJAIQuery().select(['_id', 'test_int', 'test_str', 'test_dict', 'test_list', 'test_null']).build()

        self.assertTrue(connection.is_store_exists('/find-test-store2'))
        doc_stream = document_store.find(query)
        size = 0
        for doc in doc_stream:
            size += 1
            print(doc)
        self.assertEqual(size, 0)

    def test_find_table_not_found(self):
        connection = ConnectionFactory.get_connection(connection_str=FindTest.url)
        query = OJAIQuery().select(['_id', 'test_int', 'test_str', 'test_dict', 'test_list', 'test_null']).build()
        connection.delete_store('/find-test-store3')
        self.assertFalse(connection.is_store_exists('/find-test-store3'))
        with self.assertRaises(StoreNotFoundError):
            document_store = connection.get_store(store_path='/find-test-store3')
            query_result = document_store.find(query)
            for doc in query_result:
                print(doc)

    def test_find_multiple_records(self):
        connection = ConnectionFactory.get_connection(connection_str=FindTest.url)

        if connection.is_store_exists(store_path='/find-test-store4'):
            document_store = connection.get_store(store_path='/find-test-store4')
        else:
            document_store = connection.create_store(store_path='/find-test-store4')
        document_list = []

        for i in range(1, 10):
            document_list.append(connection.new_document(dictionary={'_id': 'id00%s' % i,
                                                                     'test_int': i,
                                                                     'test_str': 'strstr',
                                                                     'test_dict': {'test_int': i},
                                                                     'test_list': [5, 6],
                                                                     'test_null': None}))

        document_store.insert_or_replace(doc_stream=document_list)
        query = OJAIQuery().select(['_id', 'test_int', 'test_str', 'test_dict', 'test_list', 'test_null']).build()
        doc_stream = document_store.find(query)

        index = 0
        for doc in doc_stream:
            self.assertEqual(doc, document_list[index].as_dictionary())
            index += 1

    def test_find_with_condition(self):
        connection = ConnectionFactory.get_connection(connection_str=FindTest.url)
        document_list = []
        for i in range(3, 7):
            document_list.append(connection.new_document(dictionary={'_id': 'id00%s' % i,
                                                                     'test_int': i,
                                                                     'test_str': 'strstr',
                                                                     'test_dict': {'test_int': i},
                                                                     'test_list': [5, 6],
                                                                     'test_null': None}))

        if connection.is_store_exists(store_path='/find-test-store4'):
            document_store = connection.get_store(store_path='/find-test-store4')
        else:
            document_store = connection.create_store(store_path='/find-test-store4')

        query = OJAIQuery().select(['_id', 'test_int', 'test_str', 'test_dict', 'test_list', 'test_null']) \
            .where(OJAIQueryCondition()
                   .and_()
                   .is_('test_int', QueryOp.GREATER_OR_EQUAL, 3)
                   .is_('test_int', QueryOp.LESS_OR_EQUAL, 6).close().close().build()).build()
        doc_stream = document_store.find(query)

        index = 0
        for doc in doc_stream:
            self.assertEqual(doc, document_list[index].as_dictionary())
            index += 1

    def test_find_all(self):
        connection = ConnectionFactory.get_connection(connection_str=FindTest.url)

        if connection.is_store_exists(store_path='/find-test-store4'):
            document_store = connection.get_store(store_path='/find-test-store4')
        else:
            document_store = connection.create_store(store_path='/find-test-store4')

        doc_stream = document_store.find()
        stream_size = 0
        for _ in doc_stream:
            stream_size += 1
        self.assertEqual(stream_size, 9)


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
