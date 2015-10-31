import unittest

from nasuta.range import Range

class TestRange(unittest.TestCase):
    def test_contains(self):
        r = Range(0, 2)
        self.assertTrue(0 in r)
        self.assertTrue(1 in r)
        self.assertTrue(2 in r)