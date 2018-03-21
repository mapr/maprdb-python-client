from __future__ import unicode_literals

from datetime import datetime

from decimal import Decimal

from ojai.o_types.OInterval import OInterval
from mapr.ojai.ojai.OJAIDocument import OJAIDocument
from ojai.o_types.ODate import ODate
from ojai.o_types.OTime import OTime
from ojai.o_types.OTimestamp import OTimestamp

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
        doc.set_id(55)
        self.assertEqual(doc.get_id(), 55)
        self.assertEqual(type(doc.get_id()), int)
        doc.set_id(long(65))
        self.assertEqual(doc.get_id(), 65)
        self.assertEqual(type(doc.get_id()), long)
        doc.set_id("75")
        self.assertEqual(doc.get_id(), "75")
        self.assertEqual(type(doc.get_id()), unicode)
        doc.set_id(str("75"))
        self.assertEqual(doc.get_id(), "75")
        self.assertEqual(type(doc.get_id()), str)

        self.assertEqual(doc.as_dictionary(), {'_id': "75"})

    def test_doc_set_date(self):
        doc = OJAIDocument()
        doc.set("today", ODate(days_since_epoch=3456))
        self.assertEqual(doc.as_dictionary(), {'today': {'$dateDay': "1979-06-19"}})
        doc.set_id("6123")
        self.assertEqual(doc.as_dictionary(), {'_id': '6123', 'today': {'$dateDay': "1979-06-19"}})

    def test_doc_set_time(self):
        doc1 = OJAIDocument().set("test_time", OTime(timestamp=1518689532)).set_id('121212')
        doc2 = OJAIDocument().set("test_time", OTime(hour_of_day=12, minutes=12, seconds=12)).set_id('121212')
        doc3 = OJAIDocument().set("test_time", OTime(date=datetime(year=1999, month=12, day=31, hour=12, minute=12,
                                                                   second=12))).set_id("121212")
        self.assertEqual(doc1.as_dictionary(), {'_id': '121212', 'test_time': {'$time': "12:12:12"}})
        self.assertEqual(doc2.as_dictionary(), {'_id': '121212', 'test_time': {'$time': "12:12:12"}})
        self.assertEqual(doc3.as_dictionary(), {'_id': '121212', 'test_time': {'$time': "12:12:12"}})

    def test_doc_set_timestamp(self):
        doc1 = OJAIDocument().set('test_timestamp', OTimestamp(millis_since_epoch=29877132000)).set_id('121212')
        doc2 = OJAIDocument().set('test_timestamp', OTimestamp(year=1970, month_of_year=12, day_of_month=12,
                                                               hour_of_day=12, minute_of_hour=12, second_of_minute=12,
                                                               millis_of_second=12)).set_id('121212')
        doc3 = OJAIDocument().set('test_timestamp', OTimestamp(date=datetime(year=1970, month=12, day=12, hour=12,
                                                                             minute=12, second=12))).set_id('121212')
        self.assertEqual(doc1.as_dictionary(), {'_id': '121212',
                                                'test_timestamp': {'$date': '1970-12-12T19:12:12.000000Z'}})
        self.assertEqual(doc2.as_dictionary(), {'_id': '121212',
                                                'test_timestamp': {'$date': '1970-12-12T12:12:12.012000Z'}})
        self.assertEqual(doc3.as_dictionary(), {'_id': '121212',
                                                'test_timestamp': {'$date': '1970-12-12T12:12:12.000000Z'}})

    def test_doc_set_interval(self):
        doc = OJAIDocument() \
            .set('test_interval', OInterval(milli_seconds=172800000))
        self.assertEqual(doc.as_dictionary(), {'test_interval': {'$interval': 172800000}})
        doc.set_id(121212) \
            .set('test_int', 123) \
            .set_id(121212) \
            .set('test_timestamp', OTimestamp(millis_since_epoch=29877132000)) \
            .set('test_float', 11.1)
        self.assertEqual(doc.as_dictionary(), {'test_interval': {'$interval': 172800000},
                                               '_id': 121212,
                                               'test_int': {'$numberLong': 123},
                                               'test_timestamp': {'$date': '1970-12-12T19:12:12.000000Z'},
                                               'test_float': {'$numberFloat': 11.1}})

    def test_doc_set_int(self):
        doc = OJAIDocument().set('test_int', 123).set_id(121212)
        self.assertEqual(doc.as_dictionary(), {'_id': 121212, 'test_int': {'$numberLong': 123}})

    def test_doc_set_bool(self):
        doc = OJAIDocument() \
            .set('test_bool', True) \
            .set('test_boolean_false', False)
        self.assertEqual(doc.as_dictionary(), {'test_bool': True, 'test_boolean_false': False})
        doc.set('test_int', 11) \
            .set('test_long', long(123))
        self.assertEqual(doc.as_dictionary(), {'test_bool': True,
                                               'test_boolean_false': False,
                                               'test_int': {'$numberLong': 11},
                                               'test_long': {'$numberLong': 123}})

    def test_doc_set_decimal(self):
        doc = OJAIDocument().set('test_decimal', Decimal(3.14))
        self.assertEqual(doc.as_dictionary(), {'test_decimal': {
            '$decimal': '3.140000000000000124344978758017532527446746826171875'}})

    def test_doc_set_float(self):
        doc = OJAIDocument() \
            .set('test_float', 11.1) \
            .set('test_float_two', 12.34)
        self.assertEqual(doc.as_dictionary(), {'test_float': {'$numberFloat': 11.1},
                                               'test_float_two': {'$numberFloat': 12.34}})
        doc.set('test_int', 999).set('test_long', long(51233123))
        self.assertEqual(doc.as_dictionary(), {'test_float': {'$numberFloat': 11.1},
                                               'test_float_two': {'$numberFloat': 12.34},
                                               'test_long': {'$numberLong': 51233123},
                                               'test_int': {'$numberLong': 999}})
        doc.set('test_bool', False)
        self.assertEqual(doc.as_dictionary(), {'test_float': {'$numberFloat': 11.1},
                                               'test_float_two': {'$numberFloat': 12.34},
                                               'test_long': {'$numberLong': 51233123},
                                               'test_int': {'$numberLong': 999},
                                               'test_bool': False})

    def test_doc_set_dict(self):
        test_dict = {'field_one': 12, 'field_two': 14}
        doc = OJAIDocument().set('test_dict', test_dict)
        self.assertEqual(doc.as_dictionary(), {'test_dict': {'field_one': {'$numberLong': 12},
                                                             'field_two': {'$numberLong': 14}}})
        doc.set_id(50)
        self.assertEqual(doc.as_dictionary(), {'_id': 50, 'test_dict': {'field_one': {'$numberLong': 12},
                                                             'field_two': {'$numberLong': 14}}})
        doc.set('test_dict.insert', 90)
        self.assertEqual(doc.as_dictionary(), {'_id': 50,
                                               'test_dict': {'field_one': {'$numberLong': 12},
                                                             'field_two': {'$numberLong': 14},
                                                             'insert': {'$numberLong': 90}}})

    def test_doc_set_byte_array(self):
        byte_array = bytearray([0x13, 0x00, 0x00, 0x00, 0x08, 0x00])
        doc = OJAIDocument().set('test_byte_array', byte_array)
        self.assertEqual(doc.as_dictionary(), {'test_byte_array': {'$binary': '\x13\x00\x00\x00\x08\x00'}})

    def test_doc_set_doc(self):
        doc_to_set = OJAIDocument().set_id(121212) \
            .set('test_int', 123) \
            .set_id(121212) \
            .set('test_timestamp', OTimestamp(millis_since_epoch=29877132000)) \
            .set('test_float', 11.1)

        doc = OJAIDocument().set('test_int_again', 55).set('internal_doc', doc_to_set)
        self.assertEqual(doc.as_dictionary(), {'test_int_again': {'$numberLong': 55},
                                               'internal_doc': {'_id': 121212,
                                                                'test_int': {'$numberLong': 123},
                                                                'test_timestamp':
                                                                    {'$date': '1970-12-12T19:12:12.000000Z'},
                                                                'test_float': {'$numberFloat': 11.1}}})

    def test_doc_set_none(self):
        doc = OJAIDocument().set('test_none', None)
        self.assertEqual(doc.as_dictionary(), {'test_none': None})

    def test_doc_delete_first_level(self):
        doc = OJAIDocument().set_id(121212) \
            .set('test_int', 123) \
            .set_id(121212) \
            .set('test_timestamp', OTimestamp(millis_since_epoch=29877132000)) \
            .set('test_float', 11.1)
        self.assertEqual(doc.as_dictionary(), {'_id': 121212,
                                               'test_int': {'$numberLong': 123},
                                               'test_timestamp': {'$date': '1970-12-12T19:12:12.000000Z'},
                                               'test_float': {'$numberFloat': 11.1}})
        doc.delete('test_timestamp')
        self.assertEqual(doc.as_dictionary(), {'_id': 121212,
                                               'test_int': {'$numberLong': 123},
                                               'test_float': {'$numberFloat': 11.1}})

    def test_doc_delete_nested(self):
        doc = OJAIDocument().set_id(121212) \
            .set('test_int', 123) \
            .set_id(121212) \
            .set('first.test_int', 1235) \
            .set('first.test_timestamp', OTimestamp(millis_since_epoch=29877132000)) \
            .set('test_float', 11.1)

        self.assertEqual(doc.as_dictionary(), {'_id': 121212,
                                               'test_int': {'$numberLong': 123},
                                               'first': {'test_timestamp': {'$date': '1970-12-12T19:12:12.000000Z'},
                                                         'test_int': {'$numberLong': 1235}},
                                               'test_float': {'$numberFloat': 11.1}})

        doc.delete('first.test_int')
        self.assertEqual(doc.as_dictionary(), {'_id': 121212,
                                               'test_int': {'$numberLong': 123},
                                               'first': {'test_timestamp': {'$date': '1970-12-12T19:12:12.000000Z'}},
                                               'test_float': {'$numberFloat': 11.1}})
        doc.delete('first.test_timestamp')
        self.assertEqual(doc.as_dictionary(), {'_id': 121212,
                                               'test_int': {'$numberLong': 123},
                                               'first': {},
                                               'test_float': {'$numberFloat': 11.1}})

    def test_doc_set_list(self):
        nested_doc = OJAIDocument().set('nested_int', 11).set('nested_str', 'strstr')
        doc = OJAIDocument().set('test_list', [1, 2, 3, 4, False, 'mystr', [{}, {}, [7, 8, 9, nested_doc]]])
        self.assertEqual(doc.as_dictionary(), {'test_list': [{'$numberLong': 1},
                                                             {'$numberLong': 2},
                                                             {'$numberLong': 3},
                                                             {'$numberLong': 4},
                                                             False,
                                                             'mystr',
                                                             [{}, {}, [{'$numberLong': 7},
                                                                       {'$numberLong': 8},
                                                                       {'$numberLong': 9},
                                                                       {
                                                                           'nested_str': 'strstr',
                                                                           'nested_int': {'$numberLong': 11}
                                                                       }
                                                                       ]
                                                              ]
                                                             ]
                                               }
                         )

    def test_doc_get(self):
        byte_array = bytearray([0x13, 0x00, 0x00, 0x00, 0x08, 0x00])
        doc = OJAIDocument().set_id(121212) \
            .set('test_int', 123) \
            .set_id(121212) \
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
            .set('first.test_binary', byte_array)

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
        self.assertEqual(doc.get_dictionary('first.test_dict'), {'a': {'$numberLong': 1}, 'b': {'$numberLong': 2}})
        self.assertEqual(doc.get_dictionary('first.test_dict2'), {})
        self.assertEqual(doc.get_list('first.test_list'), [1, 2, 'str', False, '1979-06-20'])
        self.assertEqual(doc.get_binary('first.test_binary'), '\x13\x00\x00\x00\x08\x00')

    def test_doc_set_list_tmp(self):
        recursive_doc = OJAIDocument().set('nested_int', 11).set('test_list2', [1, {'dict_list': [{'b': 55}]}])\
            .set('first.test_time', OTime(timestamp=1518689532))\
            .set('first.test_timestamp', OTimestamp(millis_since_epoch=29877132000))

        for i in range(3):
            recursive_doc = OJAIDocument().set('test_list' + str(i), [1, {'dict_list' + str(i): [{'b' + str(i): 55}, recursive_doc]}])

        nested_doc = OJAIDocument().set('nested_int', 11).set('test_list2', [1, {'dict_list': [{'b': 55}]}])\
            .set('first.test_time', OTime(timestamp=1518689532))\
            .set('first.test_timestamp', OTimestamp(millis_since_epoch=29877132000))
        doc = OJAIDocument().set('test_list', [4, [{}, {'top_list': [recursive_doc, 15, 16, 17]}, [7, 8, 9]]])
        # doc = OJAIDocument().set('test_list', [1, {'dict_list': [{'b': 55}]}])
        # print doc.as_dictionary()
        # print doc.as_json_str()


    # def test_test(self):
    #     doc = OJAIDocument().set('a.b.c', 1).set('a.b.d', 2).set('a.k.m', 3).set('a.k.c', 4)
    #     payment = {"payment_method": "card",
    #                "name": "visa",
    #                "card_info": {
    #                    "number": "1234 1234 1234 1234",
    #                    # "exp_date": ODate(date=ODate.parse("2022-10-24")),
    #                    "exp_date": ODate(year=2022, month=10, day_of_month=24),
    #                    "cvv": 123}
    #                }
    #
    #     doc.set('payment', payment)
    #     print(doc.as_dictionary())
    #
    #
    #
    # def test_date(self):
    #     t = ODate.parse("2022-10-24")
    #     # print(t)
    #     # print(t.get_year())
    #     # print(t.get_month())
    #     # print(t.get_day_of_month())
    #     # print(type(t))
    #     payment = {"payment_method": "card",
    #                "name": "visa",
    #                "card_info": {
    #                    "number": "1234 1234 1234 1234",
    #                    "exp_date": ODate(date=ODate.parse("2022-10-24")),
    #                    "cvv": 123}
    #                }
    #
    #
    #
    #     print(payment)
