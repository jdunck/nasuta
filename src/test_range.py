from datetime import datetime as dt, timedelta
import unittest

from nasuta.range import DatetimeRange, IntegerRange

class TestRange(unittest.TestCase):
    def setUp(self):
        self.r00 = IntegerRange(0, 0)
        self.r01 = IntegerRange(0, 1)
        self.r02 = IntegerRange(0, 2)
        self.r03 = IntegerRange(0, 3)
        self.r35 = IntegerRange(3, 5)
        self.r12 = IntegerRange(1, 2)
        self.r45 = IntegerRange(4, 5)
        self.r_date = DatetimeRange(dt(2013, 1, 1), dt(2014, 1, 1))

    def test_contains(self):
        self.assertFalse(0 in self.r12)
        self.assertTrue(1 in self.r12)
        self.assertTrue(2 in self.r12)
        self.assertFalse(3 in self.r12)

        r = DatetimeRange(dt(2013, 1, 1), dt(2014, 1, 1))
        self.assertFalse(
            dt(2013, 1, 1) - r.sigma in r)
        self.assertTrue(
            dt(2013, 1, 1) in r)
        self.assertTrue(
            dt(2014, 1, 1) in r)
        self.assertFalse(
            dt(2013, 1, 1) - r.sigma in r)

    def test_empty(self):
        self.assertTrue(self.r00.is_empty)
        self.assertFalse(self.r01.is_empty)

        d = dt(2013,1,1,0,0,0)
        self.assertTrue(
            DatetimeRange(d, d).is_empty)
        self.assertFalse(
            DatetimeRange(d, d + timedelta(seconds=1)).is_empty)

    def test_comparison(self):
        self.assertNotEqual(self.r01, self.r02)
        self.assertNotEqual(self.r01, self.r03)
        self.assertNotEqual(self.r01, self.r12)
        self.assertEqual(self.r01, self.r01)
        self.assertNotEqual(self.r01, self.r_date)

        self.assertFalse(self.r12 < self.r01)
        self.assertTrue(self.r02 < self.r12)

    def test_duration(self):
        self.assertEqual(0, self.r00.duration)
        self.assertEqual(2, self.r02.duration)

    def test_sentinels(self):
        self.assertEqual(self.r00.min, self.r01.min)
        self.assertTrue(self.r00.min < -2**99)
        self.assertTrue(-2**99 > self.r00.min)

        self.assertEqual(self.r00.max, self.r01.max)
        self.assertTrue(2**99 < self.r00.max)
        self.assertTrue(self.r00.max > 2**99)

    def test_unbounded(self):
        r = DatetimeRange.up_to(dt(2014,1,1))
        self.assertEqual(r.duration, r.max)
        self.assertTrue(dt(2013,1,1) in r)
        self.assertTrue(dt(1,1,1) in r)
        self.assertFalse(dt(2014,1,2) in r)

    def test_includes(self):
        self.assertTrue(self.r02.includes(self.r01))
        self.assertFalse(self.r02.includes(self.r00))
        self.assertTrue(self.r02.includes(self.r02))
        self.assertFalse(self.r02.includes(self.r03))
        self.assertTrue(self.r03.includes(self.r12))
        self.assertTrue(self.r03.includes(self.r02))

    def test_overlaps(self):
        self.assertTrue(self.r02.overlaps(self.r01))
        self.assertFalse(self.r02.overlaps(self.r00))
        self.assertTrue(self.r02.overlaps(self.r02))
        self.assertTrue(self.r02.overlaps(self.r03))
        self.assertFalse(self.r00.overlaps(self.r12))
        self.assertFalse(self.r12.overlaps(self.r00))
        self.assertFalse(self.r00.overlaps(self.r03))

    def test_eq(self):
        self.assertTrue(self.r02 == self.r02)
        self.assertFalse(self.r02 == self.r03)

    def test_gap(self):
        self.assertEqual(self.r02.gap(self.r45),
            IntegerRange(2,4))
        self.assertEqual(IntegerRange.empty, self.r02.gap(self.r01))

    def test_abuts(self):
        self.assertTrue(self.r03.abuts(self.r35))
        self.assertFalse(self.r03.abuts(self.r45))