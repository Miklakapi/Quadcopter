#!/usr/bin/env python

from unittest import TestCase

import import_from_root
from src.measurements_fix import MeasurementsFixer


class TestMeasurementsFixer(TestCase):
    def test_add_measurement(self):
        m = MeasurementsFixer()
        m.add_measurement([1.23, 1]).add_measurement([2.34, 3]).add_measurement([3.45, 2]).add_measurement([4.56, 4])
        self.assertEqual(m.get_all_measurements(), [[2.34, 3], [3.45, 2], [4.56, 4]])

    def test_get_fixed_measurement(self):
        m = MeasurementsFixer(-1)
        m.add_measurement([152.64, 0]).add_measurement([152.64, 0]).add_measurement([152.64, 0])
        self.assertEqual(m.get_fixed_measurement(), [150.00, 0])
        m.set_round(0)
        m.add_measurement([1.23, 4.56]).add_measurement([2.34, 5.67]).add_measurement([3.45, 6.78])
        self.assertEqual(m.get_fixed_measurement(), [2.0, 6.0])
        self.assertRaises(ValueError, m.set_round, -2)
