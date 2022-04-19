#!/usr/bin/env python

"""This module converts time between seconds, milliseconds and microseconds."""

from typing import TypeVar
from enum import Enum

TimeConverterObject = TypeVar('TimeConverterObject', bound='TimeConverter')


class Unit(Enum):
    def get_value(self):
        return self.value

    MIN = 1/60
    SEC = 1
    MS = 1000


class TimeConverter:
    """
    This class converts time to minutes, seconds, milliseconds and microseconds.
    """

    __seconds: float = None
    """Stores the number of seconds."""

    def __init__(self, seconds: float = 0) -> None:
        """
        This constructor writes the given time value (in seconds).

        :param seconds: float | Variable for storing and converting time
        :return: None
        """
        self.set_time(seconds)

    def set_time(self, value: float, unit: Unit = Unit.SEC) -> TimeConverterObject:
        """
        This constructor writes the given time value.

        :param value: float | Variable for storing and converting time
        :param unit: Unit | What unit of time to use
        :return: None
        """
        if value < 0:
            raise ValueError("The time cannot be negative.")
        self.__seconds = value / unit.get_value()
        return self

    def as_minutes(self) -> float:
        """
        This method returns the time in minutes.

        :return: float | Number of minutes
        """
        return self.__seconds / 60

    def as_seconds(self) -> float:
        """
        This method returns the time in seconds.

        :return: float | Number of seconds
        """
        return self.__seconds

    def as_milliseconds(self) -> int:
        """
        This method returns the time in milliseconds.

        :return: int | Number of milliseconds
        """
        return int(self.__seconds * 1000)
