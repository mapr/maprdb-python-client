from test.document.test_document import DocumentTest
from test.field_path.test_fieldpath import FieldPathTest
from test.ojaitest.test_jsonvalue import JsonValueTest
from test.o_types_test.test_odate import ODateTest
from test.o_types_test.test_ointerval import OIntervalTest
from test.o_types_test.test_otime import OTimeTest
from test.o_types_test.test_otimestamp import OTimestampTest
from test.segment.test_segment import SegmentTest
from test.values.test_type import ValueTypeTest

try:
    import unittest2 as unittest
except ImportError:
    import unittest

if __name__ == '__main__':

    test_classes_to_run = [JsonValueTest,
                           SegmentTest,
                           ODateTest,
                           OTimeTest,
                           OIntervalTest,
                           OTimestampTest,
                           ValueTypeTest,
                           FieldPathTest,
                           DocumentTest]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
