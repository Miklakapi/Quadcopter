#!/usr/bin/env python

from unittest import TestCase
from time import sleep

import import_from_root
from src.clock import Clock


class TestClock(TestCase):
    def test_elapsed_time(self):
        cl = Clock()
        sleep(1.5)
        self.assertAlmostEqual(cl.restart().as_seconds(), 1.50, 1)
        sleep(0.25)
        self.assertAlmostEqual(cl.restart().as_seconds(), 0.25, 1)
        cl.restart()
        sleep(0.5)
        self.assertAlmostEqual(cl.get_elapsed_time().as_seconds(), 0.5, 1)
        sleep(0.2)
        self.assertAlmostEqual(cl.restart().as_seconds(), 0.7, 1)
