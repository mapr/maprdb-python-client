#!/usr/bin/env python
from __future__ import unicode_literals

from ojai.types.OTime import OTime
from ojai.types.OTimestamp import OTimestamp

from mapr.ojai.ojai_query.OJAIQueryCondition import OJAIQueryCondition
from mapr.ojai.ojai_query.QueryOp import QueryOp
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class CheckAndDeleteTest(unittest.TestCase):
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
    url = "192.168.33.11:5678?auth=basic;user=root;password=r00t;" \
          "ssl=true;" \
          "sslCA=/opt/mapr/conf/ssl_truststore.pem;" \
          "sslTargetNameOverride=node1.cluster.com"

    def test_check_and_delete(self):
        connection = ConnectionFactory.get_connection(connection_str=CheckAndDeleteTest.url)
        if connection.is_store_exists(store_path='/check-delete-test-store1'):
            document_store = connection.get_store(store_path='/check-delete-test-store1')
        else:
            document_store = connection.create_store(store_path='/check-delete-test-store1')

        for doc in CheckAndDeleteTest.dict_stream:
            document_store.insert_or_replace(doc=connection.new_document(dictionary=doc))

        before_action = document_store.find_by_id('id06')
        self.assertEqual(before_action, {'_id': 'id06', 'test_int': 51, 'test_str': 'strstr'})
        document_store.check_and_delete('id06',
                                        OJAIQueryCondition().is_('test_int', QueryOp.LESS_OR_EQUAL, 52).close().build())
        after_action = document_store.find_by_id('id06')
        self.assertEqual(after_action, {})

    def test_check_and_delete_false_condition(self):
        connection = ConnectionFactory.get_connection(connection_str=CheckAndDeleteTest.url)
        if connection.is_store_exists(store_path='/check-delete-test-store1'):
            document_store = connection.get_store(store_path='/check-delete-test-store1')
        else:
            document_store = connection.create_store(store_path='/check-delete-test-store1')

        before_action = document_store.find_by_id('id07')
        self.assertEqual(before_action, {'_id': 'id07', 'test_int': 51, 'test_str': 'strstr'})
        document_store.check_and_delete('id06',
                                        OJAIQueryCondition().is_('test_int', QueryOp.LESS_OR_EQUAL, 50).close().build())
        after_action = document_store.find_by_id('id07')
        self.assertEqual(after_action, {'_id': 'id07', 'test_int': 51, 'test_str': 'strstr'})

    def test_check_and_delete_dict_condition(self):
        connection = ConnectionFactory.get_connection(connection_str=CheckAndDeleteTest.url)
        if connection.is_store_exists(store_path='/check-delete-test-store1'):
            document_store = connection.get_store(store_path='/check-delete-test-store1')
        else:
            document_store = connection.create_store(store_path='/check-delete-test-store1')

        before_action = document_store.find_by_id('id09')
        self.assertEqual(before_action, {'_id': 'id09', 'test_int': 51, 'test_str': 'strstr', 'test_list': [5, 6]})
        document_store.check_and_delete('id09',
                                        {'$eq': {'test_list': [5, 6]}})
        after_action = document_store.find_by_id('id09')
        self.assertEqual(after_action, {})
        document_store.check_and_delete('id08', {'$eq': {'test_dict.test_int': 5}})
        additional_check = document_store.find_by_id('id08')
        self.assertEqual(additional_check, {})


if __name__ == '__main__':
    test_classes_to_run = [CheckAndDeleteTest]
    loader = unittest.TestLoader()
    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
