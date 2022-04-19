#!/usr/bin/env python

"""This module measures the elapsed time."""

from time import time
from typing import TypeVar

from time_converter import TimeConverter

ClockObject = TypeVar('ClockObject', bound='Clock')


class Clock:
    """
    This class measures the elapsed time.
    """

    __time_start_point: time = None
    """Stores the time from which the class measures the elapsed time."""

    __run: bool = True
    """Keeps information whether the clock is running."""

    def __init__(self) -> None:
        """
        This constructor sets the time from which the class measures the elapsed time.
        
        :return: None
        """
        self.__time_start_point = time()

    def get_elapsed_time(self) -> TimeConverter:
        """
        This method returns the elapsed time.

        :return: TimeConverter | Elapsed time
        """
        return TimeConverter(time() - self.__time_start_point)

    def restart(self) -> TimeConverter:
        """
        This method returns the elapsed time and restarts the clock.

        :return: TimeConverter | Elapsed time
        """
        elapsed = TimeConverter(time() - self.__time_start_point)
        self.__time_start_point = time()
        return elapsed
