from datetime import datetime, timedelta
import unittest

from nasuta.range import DatetimeRange, IntegerRange

class TestRange(unittest.TestCase):
    def test_contains(self):
        r = IntegerRange(1, 2)
        self.assertFalse(0 in r)
        self.assertTrue(1 in r)
        self.assertTrue(2 in r)
        self.assertFalse(3 in r)

        r = DatetimeRange(datetime(2013, 1, 1), datetime(2014, 1, 1))
        self.assertFalse(
            datetime(2013, 1, 1) - r.sigma in r)
        self.assertTrue(
            datetime(2013, 1, 1) in r)
        self.assertTrue(
            datetime(2014, 1, 1) in r)
        self.assertFalse(
            datetime(2013, 1, 1) - r.sigma in r)

    def test_empty(self):
        self.assertTrue(IntegerRange(0, 0).is_empty)
        self.assertFalse(IntegerRange(0, 1).is_empty)

        dt = datetime(2013,1,1,0,0,0)
        self.assertTrue(
            DatetimeRange(dt,dt).is_empty)
        self.assertFalse(
            DatetimeRange(dt, dt + timedelta(seconds=1)).is_empty)
