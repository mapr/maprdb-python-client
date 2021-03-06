from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from test.document.test_document import DocumentTest
from test.document.test_document_creator import DocumentCreatorTest
from test.document.test_document_with_tags import DocumentTagsTest
from test.document.test_documentmutation import DocumentMutationTest
from test.query_test.test_query import QueryTest

try:
    import unittest2 as unittest
except ImportError:
    import unittest

if __name__ == '__main__':

    test_classes_to_run = [DocumentTest,
                           DocumentTagsTest,
                           QueryTest,
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
