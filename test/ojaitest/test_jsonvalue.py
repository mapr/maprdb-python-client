from __future__ import unicode_literals

from datetime import datetime

from struct import pack

from mapr.ojai.ojai.OJAIValue import OJAIValue
from mapr.ojai.o_types.ODate import ODate
from mapr.ojai.o_types.OInterval import OInterval
from mapr.ojai.o_types.OTime import OTime
from mapr.ojai.o_types.OTimestamp import OTimestamp
from ojai.values.Value import ValueType

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class JsonValueTest(unittest.TestCase):

    # def test_create_empty_json_value(self):
    #     json_value = JsonValue()
    #     self.assertEqual(json_value.obj_value, None)
    #     self.assertEqual(json_value.json_value, None)
    #     self.assertEqual(json_value.value_type, None)
    #     json_value.set_prim_value(55)
    #     self.assertEqual(json_value.json_value, 55)

    def test_create_type_json_value(self):
        json_value = OJAIValue(value_type=ValueType.DICTIONARY, obj_value={"a": 22, "b": 33})
        self.assertEqual(json_value.obj_value, {"a": 22, "b": 33})
        self.assertEqual(json_value.json_value, None)
        self.assertEqual(json_value.value_type, ValueType.DICTIONARY)
        self.assertEqual(json_value.get_obj(), json_value)
        self.assertTrue(json_value.check_type(ValueType.DICTIONARY))

    def test_json_value_subtypes(self):
        json_value_interval = OJAIValue(value_type=ValueType.INTERVAL, json_value=1970, obj_value=OInterval(300))
        json_value_date = OJAIValue(value_type=ValueType.DATE, json_value=1970, obj_value=ODate(days_since_epoch=300))
        json_value_time = OJAIValue(value_type=ValueType.TIME, json_value=1970, obj_value=OTime(millis_of_day=300))
        json_value_timestamp = OJAIValue(value_type=ValueType.TIMESTAMP, json_value=1970,
                                         obj_value=OTimestamp(date=datetime(1992, 3, 13)))
        self.assertTrue(isinstance(json_value_interval.get_interval(), OInterval))
        self.assertTrue(isinstance(json_value_date.get_date(), ODate))
        self.assertTrue(isinstance(json_value_time.get_time(), OTime))
        self.assertTrue(isinstance(json_value_timestamp.get_timestamp(), OTimestamp))

    def test_json_value_boolean(self):
        json_value_false = OJAIValue(value_type=ValueType.INT, bool_value=False, obj_value=123)
        self.assertEqual(json_value_false.obj_value, 123)
        self.assertEqual(json_value_false.json_value, 0)
        self.assertEqual(json_value_false.value_type, ValueType.INT)
        json_value_true = OJAIValue(value_type=ValueType.INT, bool_value=True, obj_value=123)
        self.assertEqual(json_value_true.obj_value, 123)
        self.assertEqual(json_value_true.json_value, 1)
        self.assertEqual(json_value_true.value_type, ValueType.INT)

    def test_json_value_equals(self):
        byte = pack('h', 523)
        byte2 = pack('h', 123)
        json_value_byte = OJAIValue(value_type=ValueType.BYTE, obj_value=byte, json_value=523)
        self.assertEqual(json_value_byte.obj_value, byte)
        self.assertEqual(json_value_byte.value_type, ValueType.BYTE)
        self.assertTrue(json_value_byte.__eq__(byte))
        self.assertFalse(json_value_byte.__eq__(byte2))

        json_value_int = OJAIValue(value_type=ValueType.INT, obj_value=123, json_value=123)
        self.assertEqual(json_value_int.obj_value, 123)
        self.assertEqual(json_value_int.value_type, ValueType.INT)
        self.assertTrue(json_value_int.__eq__(123))
        self.assertFalse(json_value_int.__eq__(321))

        json_value_long = OJAIValue(value_type=ValueType.LONG, obj_value=99999999999999999999999999999,
                                    json_value=99999999999999999999999999999)
        self.assertEqual(json_value_long.obj_value, 99999999999999999999999999999)
        self.assertEqual(json_value_long.value_type, ValueType.LONG)
        self.assertTrue(json_value_long.__eq__(99999999999999999999999999999))
        self.assertFalse(json_value_long.__eq__(99999999999999999999999999991))

        json_value_float = OJAIValue(value_type=ValueType.FLOAT, obj_value=123.33, json_value=123.33)
        self.assertEqual(json_value_float.obj_value, 123.33)
        self.assertEqual(json_value_float.value_type, ValueType.FLOAT)
        self.assertTrue(json_value_float.__eq__(123.33))
        self.assertFalse(json_value_float.__eq__(321.21))
        self.assertFalse(json_value_float.__eq__(321))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(JsonValueTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
