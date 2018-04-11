from mapr.ojai.ojai.OJAIDocumentCreator import OJAIDocumentCreator

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class DocumentCreatorTest(unittest.TestCase):

    def test_doc_creator_o_types(self):
        doc_string = '{"test_float": {"$numberFloat": 11.1}, "_id": "121212", "test_int": {"$numberLong": 123}, ' \
                     '"first": {"test_timestamp": {"$date": "1970-12-12T19:12:12.000000Z"}, "test_int": {' \
                     '"$numberLong": 1235}}}'
        doc = OJAIDocumentCreator.create_document(json_string=doc_string)
        self.assertEqual(doc_string, doc.as_json_str())

    def test_doc_creator_list(self):
        doc_string = '{"test_list": [{"$numberLong": 1}, {"$numberLong": 2}, {"$numberLong": 3}, {"$numberLong": 4}]}'

        doc = OJAIDocumentCreator.create_document(json_string=doc_string)
        self.assertEqual(doc_string, doc.as_json_str())

    def test_doc_creator_list_with_one_dict(self):
        doc_string = '{"_id":"id008","test_dict":{"test_int":{"$numberLong":5}},"test_int":{"$numberLong":51},' \
                    '"test_list":[{"$numberLong":5},{"$numberLong":6}],"test_null":null,"test_str":"strstr"}'

        doc = OJAIDocumentCreator.create_document(json_string=doc_string)
        self.assertEqual({'test_null': None, 'test_dict': {'test_int': 5}, 'test_list': [5, 6], '_id': u'id008',
                          'test_str': 'strstr', 'test_int': 51}, doc.as_dictionary())

