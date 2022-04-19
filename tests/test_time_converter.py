#!/usr/bin/env python

from unittest import TestCase

import import_from_root
from src.time_converter import TimeConverter, Unit


class TestTimeConverter(TestCase):
    def test_set_time(self):
        self.assertRaises(ValueError, TimeConverter, -1)
        self.assertRaises(ValueError, TimeConverter, -0.0001)

    def test_as_minutes(self):
        tc = TimeConverter(90)
        self.assertAlmostEqual(tc.as_seconds(), 90)
        self.assertAlmostEqual(tc.as_minutes(), 1.5)
        self.assertAlmostEqual(tc.as_milliseconds(), 90000)
        tc.set_time(2.5, Unit.MIN)
        self.assertAlmostEqual(tc.as_seconds(), 150)
        self.assertAlmostEqual(tc.as_minutes(), 2.5)
        self.assertAlmostEqual(tc.as_milliseconds(), 150000)
        tc.set_time(20, Unit.MS)
        self.assertAlmostEqual(tc.as_seconds(), 0.02)
        self.assertAlmostEqual(tc.as_minutes(), 0.000333, 5)
        self.assertAlmostEqual(tc.as_milliseconds(), 20)
