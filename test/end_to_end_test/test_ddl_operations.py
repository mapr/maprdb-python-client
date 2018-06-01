#!/usr/bin/env python
from __future__ import unicode_literals

from mapr.ojai.exceptions.StoreAlreadyExistsError import StoreAlreadyExistsError
from mapr.ojai.storage.OJAIDocumentStore import OJAIDocumentStore
from mapr.ojai.storage.OJAIConnection import OJAIConnection

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class ConnectionTest(unittest.TestCase):
    url = "192.168.33.11:5678?auth=basic;user=root;password=r00t;" \
          "ssl=true;" \
          "sslCA=/opt/mapr/conf/ssl_truststore.pem;" \
          "sslTargetNameOverride=node1.cluster.com"

    def test_connection(self):
        connection = OJAIConnection(connection_str=ConnectionTest.url)
        before_create = connection.is_store_exists(store_path='/test-store1')
        self.assertFalse(before_create)
        store = connection.create_store(store_path='/test-store1')
        self.assertTrue(isinstance(store, OJAIDocumentStore))
        after_create = connection.is_store_exists(store_path='/test-store1')
        self.assertTrue(after_create)
        delete_response = connection.delete_store(store_path='/test-store1')
        self.assertTrue(delete_response)

    def test_create_table_error(self):
        connection = OJAIConnection(connection_str=ConnectionTest.url)
        before_create = connection.is_store_exists(store_path='/test-store2')
        self.assertFalse(before_create)
        store = connection.create_store(store_path='/test-store2')
        self.assertTrue(isinstance(store, OJAIDocumentStore))

        self.assertTrue(connection.is_store_exists(store_path='/test-store2'))

        with self.assertRaises(StoreAlreadyExistsError):
            connection.create_store(store_path='/test-store2')

        after_create = connection.is_store_exists(store_path='/test-store2')
        self.assertTrue(after_create)
        delete_response = connection.delete_store(store_path='/test-store2')
        self.assertTrue(delete_response)


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
