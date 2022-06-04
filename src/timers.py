"""This module contains time functions."""

from typing import TypeVar
from enum import Enum
from time import sleep, time
from typing import TypeVar


ClockObject = TypeVar('ClockObject', bound='Clock')

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

    seconds: float = None
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
        self.seconds = value / unit.get_value()
        return self

    def as_minutes(self) -> float:
        """
        This method returns the time in minutes.

        :return: float | Number of minutes
        """
        return self.seconds / 60

    def as_seconds(self) -> float:
        """
        This method returns the time in seconds.

        :return: float | Number of seconds
        """
        return self.seconds

    def as_milliseconds(self) -> int:
        """
        This method returns the time in milliseconds.

        :return: int | Number of milliseconds
        """
        return int(self.seconds * 1000)


class Clock:
    """
    This class measures the elapsed time.
    """

    time_start_point: time = None
    """Stores the time from which the class measures the elapsed time."""

    run: bool = True
    """Keeps information whether the clock is running."""

    def __init__(self) -> None:
        """
        This constructor sets the time from which the class measures the elapsed time.
        
        :return: None
        """
        self.time_start_point = time()

    def get_elapsed_time(self) -> TimeConverter:
        """
        This method returns the elapsed time.

        :return: TimeConverter | Elapsed time
        """
        return TimeConverter(time() - self.time_start_point)

    def restart(self) -> TimeConverter:
        """
        This method returns the elapsed time and restarts the clock.

        :return: TimeConverter | Elapsed time
        """
        elapsed = TimeConverter(time() - self.time_start_point)
        self.time_start_point = time()
        return elapsed


class LoopRate:
    """
    This class determines the loop frequency.
    """

    frequency: int = None
    """Maximum loop frequency."""

    period: float = None
    """Maximum loop period."""

    clock: Clock = None
    """Loop clock."""

    def __init__(self, frequency: int) -> None:
        """
        This constructor sets the maximum loop frequency and loop period.

        :param frequency: int | Loop frequency
        :return: None
        """
        self.clock = Clock()
        self.set_frequency(frequency)

    def set_frequency(self, frequency: int) -> None:
        """
        This method sets the maximum loop frequency.

        :param frequency: int | Loop frequency
        :return: None
        """
        if frequency <= 0:
            raise ValueError("The frequency must be greater than 0.")
        self.frequency = frequency
        self.period = float(1/frequency)

    def slow_loop(self) -> None:
        """
        This method puts the loop to sleep if it is too fast.

        :return: None
        """
        if self.clock.get_elapsed_time().as_seconds() < self.period:
            sleep(self.period - self.clock.get_elapsed_time().as_seconds())
        self.clock.restart()
