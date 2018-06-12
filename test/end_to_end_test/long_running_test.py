#!/usr/bin/env python
from __future__ import unicode_literals

from mapr.ojai.document.OJAIDocumentMutation import OJAIDocumentMutation
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory
from test.test_utils.constants import CONNECTION_STR

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class LongRunningTest(unittest.TestCase):

    def test_huge_operations(self):
        connection = ConnectionFactory.get_connection(CONNECTION_STR)

        if connection.is_store_exists(store_path='/long-run-test-store'):
            connection.delete_store(store_path='/long-run-test-store')
        document_store = connection.create_store(store_path='/long-run-test-store')
        document_list = []
        print('Start generation.')
        for i in range(0, 10000):
            document_list.append(connection.new_document(dictionary={'_id': 'id00%s' % i,
                                                                     'test_int': i,
                                                                     'test_str': 'strstr',
                                                                     'test_dict': {'test_int': i},
                                                                     'test_list': [5, 6],
                                                                     'test_null': None}))
        print('Finish generation.')
        print('List size {0}'.format(len(document_list)))
        print('Start insert_or_replace')
        document_store.insert_or_replace(doc_stream=document_list)
        print('Finish insert_or_replace')
        print('Start replace')
        document_store.replace(doc_stream=document_list)
        print('Finish replace')
        print('Start find')
        doc_stream = document_store.find()
        print('Finish loop.')
        stream_size = 0
        print('Start loop through document stream.')
        for _ in doc_stream:
            stream_size += 1
        self.assertEqual(stream_size, 10000)
        print('Finish loop through document stream.')

        mutation = OJAIDocumentMutation().set_or_replace('test_str', 'new_string')
        print('Start update through loop.')
        for i in range(0, 10000):
            document_store.update('id00{0}'.format(i), mutation)
        print('Finish update through loop.')
        print('Start find after update.')
        doc_stream = document_store.find()
        print('Finsih find after update.')
        stream_size = 0
        print('Start loop through document stream after update.')
        for doc in doc_stream:
            stream_size += 1
            self.assertEqual(doc['test_str'], 'new_string')
        print('Finish loop through document stream after update.')

        self.assertEqual(stream_size, 10000)


if __name__ == '__main__':
    test_classes_to_run = [LongRunningTest]
    loader = unittest.TestLoader()
    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)