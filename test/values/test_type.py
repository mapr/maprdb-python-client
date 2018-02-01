from __future__ import unicode_literals

from ojai.values.Value import ValueType

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class ValueTypeTest(unittest.TestCase):

    def test_value_type(self):
        self.assertFalse(ValueType.is_numeric(ValueType.NULL))
        self.assertFalse(ValueType.is_numeric(ValueType.BOOLEAN))
        self.assertFalse(ValueType.is_numeric(ValueType.STRING))
        self.assertTrue(ValueType.is_numeric(ValueType.BYTE))
        self.assertTrue(ValueType.is_numeric(ValueType.INT))
        self.assertTrue(ValueType.is_numeric(ValueType.LONG))
        self.assertTrue(ValueType.is_numeric(ValueType.FLOAT))
        self.assertTrue(ValueType.is_numeric(ValueType.DECIMAL))
        self.assertFalse(ValueType.is_numeric(ValueType.DATE))
        self.assertFalse(ValueType.is_numeric(ValueType.TIME))
        self.assertFalse(ValueType.is_numeric(ValueType.TIMESTAMP))
        self.assertFalse(ValueType.is_numeric(ValueType.INTERVAL))
        self.assertFalse(ValueType.is_numeric(ValueType.BINARY))
        self.assertFalse(ValueType.is_numeric(ValueType.DICTIONARY))
        self.assertFalse(ValueType.is_numeric(ValueType.ARRAY))

        self.assertFalse(ValueType.is_scalar(ValueType.DICTIONARY))
        self.assertFalse(ValueType.is_scalar(ValueType.ARRAY))

        self.assertEqual(ValueType.ARRAY, ValueType.ARRAY)
        self.assertNotEqual(ValueType.ARRAY, ValueType.DICTIONARY)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ValueTypeTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
