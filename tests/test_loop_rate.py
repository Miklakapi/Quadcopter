#!/usr/bin/env python

from unittest import TestCase

import import_from_root
from src.loop_rate import LoopRate
from src.clock import Clock


class TestLoopRate(TestCase):
    def test_set_frequency(self):
        self.assertRaises(ValueError, LoopRate, -1)
        self.assertRaises(ValueError, LoopRate, 0)

    def test_slow_loop(self):
        lp = LoopRate(1)
        cl = Clock()
        while True:
            lp.slow_loop()
            et = cl.restart()
            break
        self.assertAlmostEqual(et.as_seconds(), 1.00, 1)
        lp = LoopRate(2)
        cl = Clock()
        while True:
            lp.slow_loop()
            et = cl.restart()
            break
        self.assertAlmostEqual(et.as_seconds(), 0.50, 1)
