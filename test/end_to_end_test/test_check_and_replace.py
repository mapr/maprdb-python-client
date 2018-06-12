#!/usr/bin/env python
from __future__ import unicode_literals

from mapr.ojai.ojai_query.OJAIQueryCondition import OJAIQueryCondition
from mapr.ojai.ojai_query.QueryOp import QueryOp
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory
from test.test_utils.constants import CONNECTION_STR, CONNECTION_OPTIONS, DICT_STREAM

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class CheckAndReplaceTest(unittest.TestCase):

    def test_check_and_replace(self):
        connection = ConnectionFactory.get_connection(connection_str=CONNECTION_STR,
                                                      options=CONNECTION_OPTIONS)
        if connection.is_store_exists(store_path='/check-replace-test-store1'):
            document_store = connection.get_store(store_path='/check-replace-test-store1')
        else:
            document_store = connection.create_store(store_path='/check-replace-test-store1')

        for doc in DICT_STREAM:
            document_store.insert_or_replace(doc=connection.new_document(dictionary=doc))

        before_action = document_store.find_by_id('id06')
        self.assertEqual(before_action, {'_id': 'id06', 'test_int': 51, 'test_str': 'strstr'})

        new_document = connection.new_document().set_id('id06').set('new_field', 123).set('new_array', [1, 2, 3])
        condition = OJAIQueryCondition().or_().is_('test_int', QueryOp.GREATER_OR_EQUAL, 60)\
            .is_('test_str', QueryOp.EQUAL, 'strstr')\
            .close().build()
        document_store.check_and_replace(new_document, condition)
        after_action = document_store.find_by_id('id06')
        self.assertEqual(after_action, {'_id': 'id06', 'new_field': 123, 'new_array': [1, 2, 3]})

    def test_check_and_replace_false_condition(self):
        connection = ConnectionFactory.get_connection(connection_str=CONNECTION_STR,
                                                      options=CONNECTION_OPTIONS)
        if connection.is_store_exists(store_path='/check-replace-test-store1'):
            document_store = connection.get_store(store_path='/check-replace-test-store1')
        else:
            document_store = connection.create_store(store_path='/check-replace-test-store1')

        before_action = document_store.find_by_id('id06')
        self.assertEqual(before_action, {'_id': 'id06', 'new_field': 123, 'new_array': [1, 2, 3]})

        new_document = connection.new_document().set_id('id06').set('false_field', 321).set('false_array', [5, 5, 5])
        condition = OJAIQueryCondition().or_().is_('test_int', QueryOp.GREATER_OR_EQUAL, 60)\
            .is_('test_str', QueryOp.EQUAL, 'falsestr')\
            .close().build()
        document_store.check_and_replace(new_document, condition)
        after_action = document_store.find_by_id('id06')
        self.assertEqual(after_action, {'_id': 'id06', 'new_field': 123, 'new_array': [1, 2, 3]})

    def test_check_and_replace_no_document(self):
        connection = ConnectionFactory.get_connection(connection_str=CONNECTION_STR,
                                                      options=CONNECTION_OPTIONS)
        if connection.is_store_exists(store_path='/check-replace-test-store1'):
            document_store = connection.get_store(store_path='/check-replace-test-store1')
        else:
            document_store = connection.create_store(store_path='/check-replace-test-store1')

        before_action = document_store.find_by_id('id111')
        self.assertEqual(before_action, {})

        new_document = connection.new_document().set_id('id111').set('false_field', 321).set('false_array', [5, 5, 5])
        condition = OJAIQueryCondition().or_().is_('test_int', QueryOp.GREATER_OR_EQUAL, 60)\
            .is_('test_str', QueryOp.EQUAL, 'falsestr')\
            .close().build()
        document_store.check_and_replace(new_document, condition)
        after_action = document_store.find_by_id('id111')
        self.assertEqual(after_action, {})


if __name__ == '__main__':
    test_classes_to_run = [CheckAndReplaceTest]
    loader = unittest.TestLoader()
    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
