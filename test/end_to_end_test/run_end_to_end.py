from test.end_to_end_test.test_check_and_delete import CheckAndDeleteTest
from test.end_to_end_test.test_check_and_replace import CheckAndReplaceTest
from test.end_to_end_test.test_ddl_operations import ConnectionTest
from test.end_to_end_test.test_delete_operation import DeleteTest
from test.end_to_end_test.test_find_by_id_operations import FindByIdTest
from test.end_to_end_test.test_find_operations import FindTest
from test.end_to_end_test.test_insert_replace_operations import InsertOrReplaceTest
from test.end_to_end_test.test_update_operations import UpdateTest

try:
    import unittest2 as unittest
except ImportError:
    import unittest

if __name__ == '__main__':

    test_classes_to_run = [ConnectionTest,
                           FindByIdTest,
                           FindTest,
                           InsertOrReplaceTest,
                           DeleteTest,
                           CheckAndDeleteTest,
                           CheckAndReplaceTest,
                           UpdateTest
                           ]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
