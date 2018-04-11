from mapr.ojai.ojai.OJAIDocument import OJAIDocument
from mapr.ojai.ojai.OJAIDocumentCreator import OJAIDocumentCreator
from mapr.ojai.ojai.OJAIDocumentStream import OJAIDocumentStream

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class DocumentStreamTest(unittest.TestCase):

    def test_doc_stream_iterator(self):
        # Generate list of json document
        input_list = []
        step = 0
        for i in range(1, 10):
            input_list.append(OJAIDocument()
                              .set_id('id0' + str(i))
                              .set('name', 'Jhon' + str(i))
                              .set('address.city', 'LA')
                              .set('address.street', 'street' + str(i)).as_json_str())

        doc_stream = OJAIDocumentStream(input_stream=
                                        map(lambda doc_string: OJAIDocumentCreator.create_document(doc_string),
                                            input_list))

        for doc in doc_stream:
            self.assertEqual(doc.as_json_str(), input_list[step])
            step += 1

    def test_doc_stream_interruption(self):
        """ Interrupt iteration through document stream and continuous them later"""
        input_list = []
        step = 0
        for i in range(1, 10):
            input_list.append(OJAIDocument()
                              .set_id('id0' + str(i))
                              .set('name', 'Jhon' + str(i))
                              .set('address.city', 'LA')
                              .set('address.street', 'street' + str(i)).as_json_str(with_tags=False))

        doc_stream = OJAIDocumentStream(input_stream=
                                        map(lambda doc_string: OJAIDocumentCreator.create_document(doc_string),
                                            input_list))

        for doc in doc_stream:
            self.assertEqual(doc.as_json_str(), input_list[step])
            step += 1
            if step == 5:
                break

        for doc in doc_stream:
            self.assertEqual(doc.as_json_str(), input_list[step])
            step += 1

    def test_doc_stream_type_error(self):
        with self.assertRaises(TypeError):
            OJAIDocumentStream(input_stream=[OJAIDocument()
                               .set_id('id01')
                               .set('name', 'Jhon')
                               .set('address.city', 'LA')
                               .set('address.street', 'street'), 'str', 5])
