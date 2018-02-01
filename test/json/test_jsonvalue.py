from __future__ import unicode_literals

from entity.json.JsonValue import JsonValue
from entity.o_types.ODate import ODate
from entity.o_types.OInterval import OInterval
from entity.o_types.OTime import OTime
from entity.o_types.OTimestamp import OTimestamp
from entity.values import Value
from entity.values.Value import ValueType

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class JsonValueTest(unittest.TestCase):

    def test_create_empty_json_value(self):
        json_value = JsonValue()
        self.assertEqual(json_value.obj_value, None)
        self.assertEqual(json_value.json_value, None)
        self.assertEqual(json_value.value_type, None)
        json_value.set_prim_value(55)
        self.assertEqual(json_value.json_value, 55)

    def test_create_type_json_value(self):
        json_value = JsonValue(value_type=ValueType.MAP)
        self.assertEqual(json_value.obj_value, None)
        self.assertEqual(json_value.json_value, None)
        self.assertEqual(json_value.value_type, ValueType.MAP)
        self.assertEqual(json_value.get_obj(), json_value)
        self.assertTrue(json_value.check_type(ValueType.MAP))

    def test_json_value_subtypes(self):
        json_value_interval = JsonValue(value_type=ValueType.INTERVAL, json_value=1970)
        json_value_date = JsonValue(value_type=ValueType.DATE, json_value=1970)
        json_value_time = JsonValue(value_type=ValueType.TIME, json_value=1970)
        json_value_timestamp = JsonValue(value_type=ValueType.TIMESTAMP, json_value=1970)
        self.assertTrue(isinstance(json_value_interval.get_interval(), OInterval))
        self.assertTrue(isinstance(json_value_date.get_date(), ODate))
        self.assertTrue(isinstance(json_value_time.get_time(), OTime))
        self.assertTrue(isinstance(json_value_timestamp.get_timestamp(), OTimestamp))

    def test_json_value_boolean(self):
        json_value = JsonValue(value_type=ValueType.INT, bool_value=False)
        self.assertEqual(json_value.obj_value, None)
        self.assertEqual(json_value.json_value, 0)
        self.assertEqual(json_value.value_type, ValueType.INT)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(JsonValueTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
