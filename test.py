import unittest
from script import SLCSPLookup


class TestSLCSP(unittest.TestCase):
    def test_zip_to_slcsp(self):
        lookup = SLCSPLookup()
        self.assertEqual(lookup.find_slcsp("40813"), None)
        self.assertEqual(lookup.find_slcsp("67118"), 212.35)


unittest.main()
