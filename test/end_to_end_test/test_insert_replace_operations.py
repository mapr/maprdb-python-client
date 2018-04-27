#!/usr/bin/env python
from __future__ import unicode_literals

from ojai.o_types.OTime import OTime
from ojai.o_types.OTimestamp import OTimestamp
from mapr.ojai.ojai.OJAIDocument import OJAIDocument
from mapr.ojai.ojai.OJAIDocumentStore import OJAIDocumentStore
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class InsertOrReplaceTest(unittest.TestCase):
    url = 'localhost:5678'

    def test_insert_or_replace(self):
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

        connection = ConnectionFactory.get_connection(url=InsertOrReplaceTest.url)

        if connection.is_store_exists(store_path='/test-store5'):
            document_store = connection.get_store(store_path='/test-store5')
        else:
            document_store = connection.create_store(store_path='/test-store5')
        check_store = connection.is_store_exists(store_path='/test-store5')
        self.assertTrue(check_store)
        self.assertTrue(isinstance(document_store, OJAIDocumentStore))
        for doc in dict_stream:
            document = connection.new_document(dictionary=doc)
            # print('Insert document with ID: ' + str(document.get_id()))
            document_store.insert_or_replace(doc=document)

    def test_insert(self):
        dict_stream = [{'_id': "id001", 'test_int': 51, 'test_str': 'strstr'},
                       {'_id': 'id002', 'mystr': 'str', 'test_int': 51, 'test_str': 'strstr'},
                       {'_id': 'id003', 'test_int': 51, 'test_otime': OTime(timestamp=1518689532),
                        'test_str': 'strstr'},
                       {'_id': 'id004', 'test_int': 51, 'test_timestamp': OTimestamp(millis_since_epoch=29877132000),
                        'test_str': 'strstr'},
                       {'_id': 'id005', 'test_int': 51, 'test_bool': True, 'test_str': 'strstr'},
                       {'_id': 'id006', 'test_int': 51, 'test_str': 'strstr'},
                       {'_id': 'id007', 'test_int': 51, 'test_str': 'strstr'},
                       {'_id': 'id008', 'test_int': 51, 'test_str': 'strstr', 'test_dict': {'test_int': 5}},
                       {'_id': 'id009', 'test_int': 51, 'test_str': 'strstr', 'test_list': [5, 6]},
                       {'_id': 'id010', 'test_int': 51, 'test_str': 'strstr', 'test_null': None}]

        connection = ConnectionFactory.get_connection(url=InsertOrReplaceTest.url)

        # should raise an error if exit is not 0
        if connection.is_store_exists(store_path='/test-store6'):
            document_store = connection.get_store(store_path='/test-store6')
        else:
            document_store = connection.create_store(store_path='/test-store6')
        check_store = connection.is_store_exists(store_path='/test-store6')
        self.assertTrue(check_store)
        self.assertTrue(isinstance(document_store, OJAIDocumentStore))
        for doc in dict_stream:
            document = connection.new_document(dictionary=doc)
            # print('Insert document with ID: ' + str(document.get_id()))
            document_store.insert(doc=document)
        #
        drop_store = connection.delete_store(store_path='/test-store6')
        self.assertTrue(drop_store)

    def test_replace(self):
        dict_stream = [{'_id': "id001", 'test_int': 51, 'test_str': 'strstr'},
                       {'_id': 'id002', 'mystr': 'str', 'test_int': 51, 'test_str': 'strstr'},
                       {'_id': 'id003', 'test_int': 51, 'test_otime': OTime(timestamp=1518689532),
                        'test_str': 'strstr'},
                       {'_id': 'id004', 'test_int': 51, 'test_timestamp': OTimestamp(millis_since_epoch=29877132000),
                        'test_str': 'strstr'},
                       {'_id': 'id005', 'test_int': 51, 'test_bool': True, 'test_str': 'strstr'},
                       {'_id': 'id006', 'test_int': 51, 'test_str': 'strstr'},
                       {'_id': 'id007', 'test_int': 51, 'test_str': 'strstr'},
                       {'_id': 'id008', 'test_int': 51, 'test_str': 'strstr', 'test_dict': {'test_int': 5}},
                       {'_id': 'id009', 'test_int': 51, 'test_str': 'strstr', 'test_list': [5, 6]},
                       {'_id': 'id010', 'test_int': 51, 'test_str': 'strstr', 'test_null': None}]
        dict_stream_replace = [{'_id': "id001", 'test_int': 52, 'test_str': 'strstr'},
                               {'_id': 'id002', 'mystr': 'str', 'test_int': 51, 'test_str': 'strstr'},
                               {'_id': 'id003', 'test_int': 52, 'test_otime': OTime(timestamp=1518689532),
                                'test_str': 'strstr'},
                               {'_id': 'id004', 'test_int': 52,
                                'test_timestamp': OTimestamp(millis_since_epoch=29877132000),
                                'test_str': 'strstr'},
                               {'_id': 'id005', 'test_int': 52, 'test_bool': True, 'test_str': 'strstr'},
                               {'_id': 'id006', 'test_int': 52, 'test_str': 'strstr'},
                               {'_id': 'id007', 'test_int': 52, 'test_str': 'strstr'},
                               {'_id': 'id008', 'test_int': 52, 'test_str': 'strstr', 'test_dict': {'test_int': 5}},
                               {'_id': 'id009', 'test_int': 52, 'test_str': 'strstr', 'test_list': [5, 6]},
                               {'_id': 'id010', 'test_int': 52, 'test_str': 'strstr', 'test_null': None}]

        connection = ConnectionFactory.get_connection(url=InsertOrReplaceTest.url)

        # should raise an error if exit is not 0
        if connection.is_store_exists(store_path='/test-store7'):
            document_store = connection.get_store(store_path='/test-store7')
        else:
            document_store = connection.create_store(store_path='/test-store7')
        check_store = connection.is_store_exists(store_path='/test-store7')
        self.assertTrue(check_store)
        self.assertTrue(isinstance(document_store, OJAIDocumentStore))
        for doc in dict_stream:
            document = connection.new_document(dictionary=doc)
            # print('Insert document with ID: ' + str(document.get_id()))
            document_store.insert(doc=document)

        for doc in dict_stream_replace:
            document = connection.new_document(dictionary=doc)
            # print('Insert document with ID: ' + str(document.get_id()))
            document_store.replace(doc=document)

        drop_store = connection.delete_store(store_path='/test-store7')
        self.assertTrue(drop_store)

    def test_nested_doc_insert(self):
        nested_doc = OJAIDocument().set('nested_int', 11).set('nested_str', 'strstr')
        doc = OJAIDocument().set('test_list', [1, 2, 3, 4, False, 'mystr', [{}, {}, [7, 8, 9, nested_doc]]]) \
            .set_id('testid001')
        connection = ConnectionFactory.get_connection(url=InsertOrReplaceTest.url)
        if connection.is_store_exists(store_path='/test-store8'):
            document_store = connection.get_store(store_path='/test-store8')
        else:
            document_store = connection.create_store(store_path='/test-store8')
        check_store = connection.is_store_exists(store_path='/test-store8')
        self.assertTrue(check_store)
        self.assertTrue(isinstance(document_store, OJAIDocumentStore))

        document_store.insert_or_replace(doc=doc)


if __name__ == '__main__':
    test_classes_to_run = [InsertOrReplaceTest]
    loader = unittest.TestLoader()
    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
