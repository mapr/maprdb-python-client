from __future__ import unicode_literals

from random import getrandbits, randint

from ojai.types.OInterval import OInterval
from mapr.ojai.ojai.OJAIDocument import OJAIDocument
from ojai.types.ODate import ODate
from ojai.types.OTime import OTime
from ojai.types.OTimestamp import OTimestamp

from mapr.ojai.ojai_utils.ojai_document_creator import OJAIDocumentCreator

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class DocumentTest(unittest.TestCase):

    def test_empty_doc(self):
        doc = OJAIDocument()
        self.assertTrue(doc.empty())
        self.assertEqual(doc.as_dictionary(), {})

    def test_doc_insert_id(self):
        doc = OJAIDocument()
        doc.set_id("75")
        self.assertEqual(doc.get_id(), "75")
        self.assertEqual(type(doc.get_id()), unicode)
        doc.set_id(str("75"))
        self.assertEqual(doc.get_id(), "75")
        self.assertEqual(type(doc.get_id()), str)

        self.assertEqual(doc.as_dictionary(), {'_id': "75"})

    def test_doc_set_int(self):
        doc = OJAIDocument().set('test_int', 123).set_id('121212')
        self.assertEqual(doc.as_dictionary(), {'_id': '121212', 'test_int': 123})

    def test_doc_set_bool(self):
        doc = OJAIDocument() \
            .set('test_bool', True) \
            .set('test_boolean_false', False)
        self.assertEqual(doc.as_dictionary(), {'test_bool': True, 'test_boolean_false': False})
        doc.set('test_int', 11) \
            .set('test_long', long(123))
        self.assertEqual(doc.as_dictionary(), {'test_bool': True,
                                               'test_boolean_false': False,
                                               'test_int': 11,
                                               'test_long': 123})

    def test_doc_set_float(self):
        doc = OJAIDocument() \
            .set('test_float', 11.1) \
            .set('test_float_two', 12.34)
        self.assertEqual(doc.as_dictionary(), {'test_float': 11.1,
                                               'test_float_two': 12.34})
        doc.set('test_int', 999).set('test_long', long(51233123))
        self.assertEqual(doc.as_dictionary(), {'test_float': 11.1,
                                               'test_float_two': 12.34,
                                               'test_long': 51233123,
                                               'test_int': 999})
        doc.set('test_bool', False)
        self.assertEqual(doc.as_dictionary(), {'test_float': 11.1,
                                               'test_float_two': 12.34,
                                               'test_long': 51233123,
                                               'test_int': 999,
                                               'test_bool': False})

    def test_doc_set_dict(self):
        test_dict = {'field_one': 12, 'field_two': 14}
        doc = OJAIDocument().set('test_dict', test_dict)
        self.assertEqual(doc.as_dictionary(), {'test_dict': {'field_one': 12,
                                                             'field_two': 14}})
        doc.set_id('50')
        self.assertEqual(doc.as_dictionary(), {'_id': '50', 'test_dict': {'field_one': 12,
                                                                          'field_two': 14}})
        doc.set('test_dict.insert', 90)
        self.assertEqual(doc.as_dictionary(), {'_id': '50',
                                               'test_dict': {'field_one': 12,
                                                             'field_two': 14,
                                                             'insert': 90}})

    def test_doc_set_byte_array(self):
        byte_array = bytearray([0x13, 0x00, 0x00, 0x00, 0x08, 0x00])
        doc = OJAIDocument().set('test_byte_array', byte_array)
        self.assertEqual(doc.as_dictionary(), {'test_byte_array': bytearray(b'\x13\x00\x00\x00\x08\x00')})
        self.assertEqual(doc.as_json_str(),
                         '{"test_byte_array": {"$binary": "EwAAAAgA"}}')

        recreated_doc = OJAIDocumentCreator().create_document(doc.as_json_str())
        self.assertEqual(recreated_doc.as_dictionary(), {'test_byte_array': bytearray(b'\x13\x00\x00\x00\x08\x00')})

    def test_doc_set_none(self):
        doc = OJAIDocument().set('test_none', None)
        self.assertEqual(doc.as_dictionary(), {'test_none': None})

    def test_doc_delete_first_level(self):
        doc = OJAIDocument().set_id('121212') \
            .set('test_int', 123) \
            .set('test_float', 11.1)
        self.assertEqual(doc.as_dictionary(), {'_id': '121212',
                                               'test_int': 123,
                                               'test_float': 11.1})
        doc.delete('test_timestamp')
        self.assertEqual(doc.as_dictionary(), {'_id': '121212',
                                               'test_int': 123,
                                               'test_float': 11.1})

    def test_delete_by_index(self):
        doc = OJAIDocument().set('test_list',
                                 [1, 2, 3, 4, 5, 6, 7])

        self.assertEqual({'test_list': [1, 2, 3, 4, 5, 6, 7]},
                         doc.as_dictionary())
        doc.delete('test_list[3]')
        self.assertEqual({'test_list': [1, 2, 3, 5, 6, 7]},
                         doc.as_dictionary())

    def test_doc_delete_nested(self):
        doc = OJAIDocument().set_id('121212') \
            .set('test_int', 123) \
            .set('first.test_int', 1235) \
            .set('first.test_float', 12.2) \
            .set('test_float', 11.1)

        self.assertEqual(doc.as_dictionary(), {'_id': '121212',
                                               'test_int': 123,
                                               'first': {'test_float': 12.2,
                                                         'test_int': 1235},
                                               'test_float': 11.1})

        doc.delete('first.test_int')
        self.assertEqual(doc.as_dictionary(), {'_id': '121212',
                                               'test_int': 123,
                                               'first': {'test_float': 12.2},
                                               'test_float': 11.1})
        doc.delete('first.test_float')
        self.assertEqual(doc.as_dictionary(), {'_id': '121212',
                                               'test_int': 123,
                                               'first': {},
                                               'test_float': 11.1})

    def set_random_bytearray(self):
        arr_len = randint(10, 100)
        val = bytearray(getrandbits(8) for i in range(arr_len))
        return val

    def test_byte_array(self):
        b = self.set_random_bytearray()
        doc = OJAIDocument().set('b_array', b)

    def test_doc_set_list(self):
        nested_doc = OJAIDocument().set('nested_int', 11).set('nested_str', 'strstr')
        doc = OJAIDocument().set('test_list', [1, 2, 3, 4, False, 'mystr', [{}, {}, [7, 8, 9, nested_doc]]])
        self.assertEqual(doc.as_dictionary(), {'test_list': [1,
                                                             2,
                                                             3,
                                                             4,
                                                             False,
                                                             'mystr',
                                                             [{}, {}, [7, 8, 9,
                                                                       {
                                                                           'nested_str': 'strstr',
                                                                           'nested_int': 11
                                                                       }
                                                                       ]
                                                              ]
                                                             ]
                                               }
                         )

    def test_doc_get(self):
        doc = OJAIDocument().set_id('121212') \
            .set('test_int', 123) \
            .set('first.test_int', 1235) \
            .set('first.test_long', 123456789) \
            .set('first.test_float', 123456789.123) \
            .set('first.test_time', OTime(timestamp=1518689532)) \
            .set('test_float', 11.1) \
            .set('first.test_timestamp', OTimestamp(millis_since_epoch=29877132000)) \
            .set('first.test_date', ODate(days_since_epoch=3456)) \
            .set('first.test_interval', OInterval(milli_seconds=172800000)) \
            .set('first.test_bool', True) \
            .set('first.test_bool_false', False) \
            .set('first.test_invalid', ODate(days_since_epoch=3457)) \
            .set('first.test_str', 'strstr') \
            .set('first.test_dict', {'a': 1, 'b': 2}) \
            .set('first.test_dict2', {}) \
            .set('first.test_list', [1, 2, 'str', False, ODate(days_since_epoch=3457)]) \

        self.assertEqual(doc.get_int('test_int'), 123)
        self.assertEqual(doc.get_int('first.test_int'), 1235)
        self.assertEqual(doc.get_int('first.test_long'), 123456789)
        self.assertEqual(doc.get_long('first.test_long'), 123456789)
        self.assertEqual(doc.get_float('first.test_float'), 123456789.123)
        self.assertEqual(doc.get_time('first.test_time').time_to_str(), '12:12:12')
        self.assertEqual(doc.get_interval('first.test_interval').time_duration, 172800000)
        self.assertEqual(doc.get_timestamp('first.test_timestamp').__str__(), '1970-12-12T19:12:12.000000Z')
        self.assertEqual(doc.get_date('first.test_date').to_date_str(), '1979-06-19')
        self.assertEqual(doc.get_boolean('first.test_bool'), True)
        self.assertEqual(doc.get_boolean('first.test_bool_false'), False)
        self.assertEqual(doc.get_boolean('first.test_invalid'), None)
        self.assertEqual(doc.get_str('first.test_str'), 'strstr')
        self.assertEqual(doc.get_dictionary('first.test_dict'), {'a': 1, 'b': 2})
        self.assertEqual(doc.get_dictionary('first.test_dict2'), {})

    # MAPRDB-779
    def test_document_change_value_type(self):
        doc = OJAIDocument().set_id('121212') \
            .set('test_int', 123) \
            .set('test_float', 11.1)
        self.assertEqual(doc.as_dictionary(), {'_id': '121212',
                                               'test_int': 123,
                                               'test_float': 11.1})
        doc.set('test_int', 12.2)

        self.assertEqual(doc.as_dictionary(), {'_id': '121212',
                                               'test_int': 12.2,
                                               'test_float': 11.1})

    def test_get_bytearray(self):
        b = bytearray([0x13, 0x00, 0x00, 0x00, 0x08, 0x00])
        doc = OJAIDocument()
        doc.set('f1', b)
        self.assertEqual(doc.get_binary('f1'), b)

    def test_set_list_instead_of_list(self):
        doc = OJAIDocument()
        field = 'list_field'
        doc.set(field, value=[1, 1])
        doc.set(field, value=[2, 2])
        self.assertEqual(doc.as_dictionary(), {field: [2, 2]})
        doc.set(field, 5)
        self.assertEqual(doc.as_dictionary(), {field: 5})
        doc.set(field, value=[1, 1])
        self.assertEqual(doc.as_dictionary(), {field: [1, 1]})

    def test_set_array_element(self):
        doc = OJAIDocument().set('a.b.c', [1, 2, 3])
        self.assertEqual(doc.as_dictionary(), {'a': {'b': {'c': [1, 2, 3]}}})
        doc.set('a.b.c[1]', 9)
        self.assertEqual(doc.as_dictionary(), {'a': {'b': {'c': [1, 9, 3]}}})
        doc.set('a.b.c[100]', 55)
        self.assertEqual(doc.as_dictionary(), {'a': {'b': {'c': [1, 9, 3, 55]}}})
        self.assertEqual(doc.get('a.b.c[55]'), None)
        self.assertEqual(doc.get('a.b.c[0]'), 1)
        self.assertEqual(doc.get('a.b.c[1]'), 9)
        self.assertEqual(doc.get('a.b.c[3]'), 55)

    def test_document_to_json_str_without_tags(self):
        doc = OJAIDocument().set_id('121212') \
            .set('test_int', 123) \
            .set('first.test_int', 1235) \
            .set('first.test_long', 123456789) \
            .set('first.test_float', 123456789.123) \
            .set('first.test_time', OTime(timestamp=1518689532)) \
            .set('test_float', 11.1) \
            .set('first.test_timestamp', OTimestamp(millis_since_epoch=29877132000)) \
            .set('first.test_date', ODate(days_since_epoch=3456)) \
            .set('first.test_bool', True) \
            .set('first.test_bool_false', False) \
            .set('first.test_invalid', ODate(days_since_epoch=3457)) \
            .set('first.test_str', 'strstr') \
            .set('first.test_dict', {'a': 1, 'b': 2}) \
            .set('first.test_dict2', {}) \
            .set('first.test_list', [1, 2, 'str', False, ODate(days_since_epoch=3457)])\
            .set('test_bytearray', bytearray(b'\x06\x06'))

        self.assertEqual('{"test_float": 11.1, '
                         '"_id": "121212", '
                         '"test_bytearray": "\\u0006\\u0006", '
                         '"test_int": 123, '
                         '"first": {"test_invalid": "1979-06-20", '
                         '"test_time": "12:12:12", '
                         '"test_bool_false": false, '
                         '"test_date": "1979-06-19", '
                         '"test_long": 123456789, '
                         '"test_dict2": {}, '
                         '"test_dict": {"a": 1, "b": 2}, '
                         '"test_bool": true, '
                         '"test_list": [1, 2, "str", false, "1979-06-20"], '
                         '"test_float": 123456789.123, '
                         '"test_timestamp": "1970-12-12T19:12:12.000000Z", '
                         '"test_str": "strstr", '
                         '"test_int": 1235}}',
                         doc.as_json_str(with_tags=False))
