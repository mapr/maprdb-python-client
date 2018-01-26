from __future__ import unicode_literals

from entity.o_types.ODate import ODate

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class ODateTest(unittest.TestCase):

    def test_days_from_epoch(self):
        pass


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ODateTest)
    unittest.TextTestRunner(verbosity=2).run(suite)



