#!/usr/bin/env python
from __future__ import unicode_literals

from mapr.ojai.ojai.OJAIDocument import OJAIDocument
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory
from test.test_utils.constants import CONNECTION_STR, CONNECTION_OPTIONS, DICT_STREAM

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class DeleteTest(unittest.TestCase):

    def test_delete_document(self):
        connection = ConnectionFactory.get_connection(connection_str=CONNECTION_STR,
                                                      options=CONNECTION_OPTIONS)

        if connection.is_store_exists(store_path='/delete-test-store1'):
            document_store = connection.get_store(store_path='/delete-test-store1')
        else:
            document_store = connection.create_store(store_path='/delete-test-store1')

        document = None

        for doc in DICT_STREAM:
            document = connection.new_document(dictionary=doc)
            document_store.insert_or_replace(doc=document)

        document_store.delete(doc=document)
        self.assertEqual(document_store.find_by_id('id10'), {})

    def test_delete_id(self):
        connection = ConnectionFactory.get_connection(connection_str=CONNECTION_STR,
                                                      options=CONNECTION_OPTIONS)

        if connection.is_store_exists(store_path='/delete-test-store1'):
            document_store = connection.get_store(store_path='/delete-test-store1')
        else:
            document_store = connection.create_store(store_path='/delete-test-store1')

        document_store.delete(_id='id09')

        self.assertEqual(document_store.find_by_id('id09'), {})

    def test_delete_document_stream(self):
        connection = ConnectionFactory.get_connection(connection_str=CONNECTION_STR,
                                                      options=CONNECTION_OPTIONS)

        if connection.is_store_exists(store_path='/delete-test-store1'):
            document_store = connection.get_store(store_path='/delete-test-store1')
        else:
            document_store = connection.create_store(store_path='/delete-test-store1')

        doc_stream = []

        for i in range(1, 5):
            doc_stream.append(OJAIDocument().from_dict(DICT_STREAM[i]))

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
