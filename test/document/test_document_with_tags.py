from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library

standard_library.install_aliases()
from builtins import *
import json
from datetime import datetime

from ojai.types.OInterval import OInterval
from mapr.ojai.ojai.OJAIDocument import OJAIDocument
from ojai.types.ODate import ODate
from ojai.types.OTime import OTime
from ojai.types.OTimestamp import OTimestamp

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class DocumentTagsTest(unittest.TestCase):

    def test_empty_doc(self):
        doc = OJAIDocument()
        self.assertTrue(doc.empty())
        self.assertEqual(doc.as_dictionary(), {})

    def test_doc_insert_id(self):
        doc = OJAIDocument()
        doc.set_id("75")
        self.assertEqual(doc.get_id(), "75")
        self.assertIsInstance(doc.get_id(), str)
        doc.set_id(str("75"))
        self.assertIsInstance(doc.get_id(), str)
        self.assertEqual(doc.get_id(), "75")
        #
        self.assertEqual(doc.as_dictionary(), {'_id': "75"})

    def test_doc_set_date(self):
        doc = OJAIDocument()
        doc.set("today", ODate(days_since_epoch=3456))
        self.assertEqual(doc.as_json_str(), json.dumps({"today": {"$dateDay": "1979-06-19"}}))
        doc.set_id("6123")
        self.assertEqual(json.loads(doc.as_json_str()), {"_id": "6123", "today": {"$dateDay": "1979-06-19"}})

    def test_doc_set_time(self):
        doc1 = OJAIDocument().set("test_time", OTime(timestamp=1518689532)).set_id('121212')
        doc2 = OJAIDocument().set("test_time", OTime(hour_of_day=12, minutes=12, seconds=12)).set_id('121212')
        doc3 = OJAIDocument().set("test_time", OTime(date=datetime(year=1999, month=12, day=31, hour=12, minute=12,
                                                                   second=12))).set_id("121212")
        self.assertEqual(doc1.as_json_str(), json.dumps({"test_time": {"$time": "12:12:12"}, "_id": "121212"}))
        self.assertEqual(doc2.as_json_str(), json.dumps({"test_time": {"$time": "12:12:12"}, "_id": "121212"}))
        self.assertEqual(doc3.as_json_str(), json.dumps({"test_time": {"$time": "12:12:12"}, "_id": "121212"}))

    def test_doc_set_timestamp(self):
        doc1 = OJAIDocument().set('test_timestamp', OTimestamp(millis_since_epoch=29877132000)).set_id('121212')
        doc2 = OJAIDocument().set('test_timestamp', OTimestamp(year=1970, month_of_year=12, day_of_month=12,
                                                               hour_of_day=12, minute_of_hour=12, second_of_minute=12,
                                                               millis_of_second=12)).set_id('121212')
        doc3 = OJAIDocument().set('test_timestamp', OTimestamp(date=datetime(year=1970, month=12, day=12, hour=12,
                                                                             minute=12, second=12))).set_id('121212')
        self.assertEqual(doc1.as_json_str(), json.dumps({"test_timestamp": {"$date": "1970-12-12T19:12:12.000000Z"},
                                                         "_id": "121212"}))
        self.assertEqual(doc2.as_json_str(), json.dumps({"test_timestamp": {"$date": "1970-12-12T12:12:12.012000Z"},
                                                         "_id": "121212"}))
        self.assertEqual(doc3.as_json_str(),
                         json.dumps({"test_timestamp": {"$date": "1970-12-12T12:12:12.000000Z"}, "_id": "121212"}))

    def test_doc_set_interval(self):
        doc = OJAIDocument() \
            .set('test_interval', OInterval(milli_seconds=172800000))
        self.assertEqual(doc.as_json_str(), '{"test_interval": {"$interval": 172800000}}')
        doc.set_id('121212') \
            .set('test_int', 123) \
            .set('test_timestamp', OTimestamp(millis_since_epoch=29877132000)) \
            .set('test_float', 11.1)
        json.loads(doc.as_json_str())
        self.assertEqual(doc.as_json_str(), json.dumps({"test_interval": {"$interval": 172800000}, "_id": "121212",
                                                        "test_int": {"$numberLong": 123},
                                                        "test_timestamp": {"$date": "1970-12-12T19:12:12.000000Z"},
                                                        "test_float": {"$numberFloat": 11.1}}))

    def test_doc_set_int(self):
        doc = OJAIDocument().set('test_int', 123).set_id('121212')
        self.assertEqual(doc.as_json_str(), json.dumps({"test_int": {"$numberLong": 123}, "_id": "121212"}))

    def test_doc_set_bool(self):
        doc = OJAIDocument() \
            .set('test_bool', True) \
            .set('test_boolean_false', False)
        self.assertEqual(doc.as_json_str(), '{"test_bool": true, "test_boolean_false": false}')
        doc.set('test_int', 11) \
            .set('test_long', int(123))
        self.assertEqual(doc.as_json_str(), json.dumps({"test_bool": True, "test_boolean_false": False,
                                                        "test_int": {"$numberLong": 11},
                                                        "test_long": {"$numberLong": 123}}))

    def test_doc_set_float(self):
        doc = OJAIDocument() \
            .set('test_float', 11.1) \
            .set('test_float_two', 12.34)
        self.assertEqual(doc.as_json_str(), json.dumps({"test_float": {"$numberFloat": 11.1}, "test_float_two": {
            "$numberFloat": 12.34}}))
        doc.set('test_int', 999).set('test_long', int(51233123))
        self.assertEqual(json.loads(doc.as_json_str()), {"test_float": {"$numberFloat": 11.1},
                                                         "test_long": {"$numberLong": 51233123},
                                                         "test_float_two": {"$numberFloat": 12.34},
                                                         "test_int": {"$numberLong": 999}})
        doc.set('test_bool', False)
        self.assertEqual(doc.as_json_str(), json.dumps({"test_float": {"$numberFloat": 11.1},
                                                        "test_float_two": {"$numberFloat": 12.34},
                                                        "test_int": {"$numberLong": 999},
                                                        "test_long": {"$numberLong": 51233123}, "test_bool": False}))

    def test_doc_set_dict(self):
        test_dict = {'field_one': 12, 'field_two': 14}
        doc = OJAIDocument().set('test_dict', test_dict)
        self.assertEqual(doc.as_json_str(), json.dumps({"test_dict": {"field_one": {"$numberLong": 12}, "field_two": {
            "$numberLong": 14}}}))
        doc.set_id('50')
        self.assertEqual(doc.as_json_str(), json.dumps({"test_dict": {"field_one": {"$numberLong": 12},
                                                                      "field_two": {"$numberLong": 14}}, "_id": "50"}))
        doc.set('test_dict.insert', 90)
        self.assertEqual(doc.as_json_str(), json.dumps({"test_dict": {"field_one": {"$numberLong": 12},
                                                                      "field_two": {"$numberLong": 14},
                                                                      "insert": {"$numberLong": 90}}, "_id": "50"}))

    def test_doc_set_byte_array(self):
        byte_array = bytearray([0x13, 0x00, 0x00, 0x00, 0x08, 0x00])
        doc = OJAIDocument().set('test_byte_array', byte_array)
        self.assertEqual(doc.as_json_str(),
                         json.dumps({"test_byte_array": {"$binary": "EwAAAAgA"}}))

    def test_doc_set_doc(self):
        doc_to_set = OJAIDocument().set_id('121212') \
            .set('test_int', 123) \
            .set('test_timestamp', OTimestamp(millis_since_epoch=29877132000)) \
            .set('test_float', 11.1)

        doc = OJAIDocument().set('test_int_again', 55).set('internal_doc', doc_to_set)
        self.assertEqual(doc.as_json_str(), json.dumps({"test_int_again": {"$numberLong": 55},
                                                        "internal_doc": {"_id": "121212",
                                                                         "test_int": {"$numberLong": 123},
                                                                         "test_timestamp": {
                                                                             "$date": "1970-12-12T19:12:12.000000Z"},
                                                                         "test_float": {"$numberFloat": 11.1}}}))

    def test_doc_set_none(self):
        doc = OJAIDocument().set('test_none', None)
        self.assertEqual(json.dumps({"test_none": None}), doc.as_json_str())

    def test_doc_delete_first_level(self):
        doc = OJAIDocument().set_id('121212') \
            .set('test_int', 123) \
            .set('test_timestamp', OTimestamp(millis_since_epoch=29877132000)) \
            .set('test_float', 11.1)
        self.assertEqual(doc.as_json_str(), json.dumps({"_id": "121212", "test_int": {"$numberLong": 123},
                                                        "test_timestamp": {"$date": "1970-12-12T19:12:12.000000Z"},
                                                        "test_float": {"$numberFloat": 11.1}}))
        doc.delete('test_timestamp')
        self.assertEqual(doc.as_json_str(), json.dumps({"_id": "121212", "test_int": {"$numberLong": 123},
                                                        "test_float": {"$numberFloat": 11.1}}))

    def test_doc_delete_nested(self):
        doc = OJAIDocument().set_id('121212') \
            .set('test_int', 123) \
            .set('first.test_int', 1235) \
            .set('first.test_timestamp', OTimestamp(millis_since_epoch=29877132000)) \
            .set('test_float', 11.1)

        self.assertEqual(doc.as_json_str(), json.dumps({"_id": "121212", "test_int": {"$numberLong": 123},
                                                        "first": {"test_int": {"$numberLong": 1235},
                                                                  "test_timestamp": {
                                                                      "$date": "1970-12-12T19:12:12.000000Z"}},
                                                        "test_float": {"$numberFloat": 11.1}}))

        doc.delete('first.test_int')
        self.assertEqual(doc.as_json_str(), json.dumps({"_id": "121212", "test_int": {"$numberLong": 123},
                                                        "first": {
                                                            "test_timestamp": {"$date": "1970-12-12T19:12:12.000000Z"}},
                                                        "test_float": {"$numberFloat": 11.1}}))
        doc.delete('first.test_timestamp')
        self.assertEqual(doc.as_json_str(), json.dumps({"_id": "121212", "test_int": {"$numberLong": 123},
                                                        "first": {}, "test_float": {"$numberFloat": 11.1}}))

    def test_doc_set_list(self):
        nested_doc = OJAIDocument().set('nested_int', 11).set('nested_str', 'strstr')
        doc = OJAIDocument().set('test_list', [1, 2, 3, 4, False, 'mystr', [{}, {}, [7, 8, 9, nested_doc]]])
        self.assertEqual(doc.as_json_str(), json.dumps({"test_list": [{"$numberLong": 1}, {"$numberLong": 2},
                                                                      {"$numberLong": 3}, {"$numberLong": 4}, False,
                                                                      "mystr",
                                                                      [{}, {}, [{"$numberLong": 7}, {"$numberLong": 8},
                                                                                {"$numberLong": 9},
                                                                                {"nested_int": {"$numberLong": 11},
                                                                                 "nested_str": "strstr"}]]]}))

    # MAPRDB-779
    def test_document_change_value_type(self):
        doc = OJAIDocument().set_id('121212') \
            .set('test_int', 123) \
            .set('test_float', 11.1)
        self.assertEqual(doc.as_json_str(), json.dumps({"_id": "121212", "test_int": {"$numberLong": 123},
                                                        "test_float": {"$numberFloat": 11.1}}))
        doc.set('test_int', OTimestamp(millis_since_epoch=29877132000))

        self.assertEqual(doc.as_json_str(),
                         json.dumps({"_id": "121212", "test_int": {"$date": "1970-12-12T19:12:12.000000Z"},
                                     "test_float": {"$numberFloat": 11.1}}))

    def test_set_dict_instead_of_dict(self):
        doc = OJAIDocument()
        field = 'dict_field'
        doc.set(field, value={'n': 2})
        doc.set(field, value={'r': 3})
        self.assertEqual(json.loads(doc.as_json_str()), {field: {'r': {'$numberLong': 3}}})

    def test_set_list_instead_of_list(self):
        doc = OJAIDocument()
        field = 'list_field'
        doc.set(field, value=[1, 1])
        self.assertEqual(doc.as_json_str(), json.dumps({"list_field": [{"$numberLong": 1}, {"$numberLong": 1}]}))
        doc.set(field, value=[2, 2])
        self.assertEqual(doc.as_json_str(), json.dumps({"list_field": [{"$numberLong": 2}, {"$numberLong": 2}]}))

    # MAPRDB-1512
    def test_list_with_nested_dict(self):
        test_doc_dict = {"_id": "some_id", "list": [{"name": 55,
                                                     "surname": "Surname",
                                                     "city": "City"}]}
        doc = OJAIDocument().from_dict(test_doc_dict)
        self.assertEqual(doc.as_dictionary(),
                         {'_id': 'some_id', 'list': [{'city': 'City', 'surname': 'Surname', 'name': 55}]})
        self.assertEqual(doc.as_json_str(),
                         json.dumps({"_id": "some_id", "list": [{"name": {"$numberLong": 55},
                                                                 "surname": "Surname", "city": "City"}]}))
        self.assertEqual(doc.as_json_str(with_tags=False),
                         json.dumps({"_id": "some_id", "list": [{"name": 55, "surname": "Surname", "city": "City"}]}))

    def test_list_with_nested_complex_dicts(self):
        test_doc_dict = {"_id": "some_id", "list": [{"age": 55,
                                                     "name": {"surname": "Surname",
                                                              "firstname": "firstname"}}]}
        doc = OJAIDocument().from_dict(test_doc_dict)
        self.assertEqual(doc.as_dictionary(),
                         {'_id': 'some_id', 'list': [{'age': 55, "name": {'firstname': 'firstname', 'surname': 'Surname'}}]})
        self.assertEqual(doc.as_json_str(),
                         json.dumps({"_id": "some_id", "list": [{"age": {"$numberLong": 55},
                                                                 "name": {"surname": "Surname", "firstname": "firstname"}}]}))
        self.assertEqual(doc.as_json_str(with_tags=False),
                         json.dumps({"_id": "some_id", "list": [{"age": 55, "name": {"surname": "Surname", "firstname": "firstname"}}]}))
