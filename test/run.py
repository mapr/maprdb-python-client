from test.document.test_document import DocumentTest
from test.document.test_document_creator import DocumentCreatorTest
from test.document.test_document_with_tags import DocumentTagsTest
from test.document.test_documentmutation import DocumentMutationTest
from test.document.test_documentstream import DocumentStreamTest
from test.ojaitest.test_jsonvalue import JsonValueTest
from test.query_test.test_query import QueryTest
from test.values.test_type import ValueTypeTest

try:
    import unittest2 as unittest
except ImportError:
    import unittest

if __name__ == '__main__':

    test_classes_to_run = [JsonValueTest,
                           ValueTypeTest,
                           DocumentTest,
                           DocumentTagsTest,
                           QueryTest,
                           DocumentStreamTest,
                           DocumentCreatorTest,
                           DocumentMutationTest
                           ]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
