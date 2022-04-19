#!/usr/bin/env python

"""This module managed the loop frequency to limit the loop speed."""

from time import sleep

from clock import Clock


class LoopRate:
    """
    This class determines the loop frequency.
    """

    __frequency: int = None
    """Maximum loop frequency."""

    __period: float = None
    """Maximum loop period."""

    __clock: Clock = None
    """Loop clock."""

    def __init__(self, frequency: int) -> None:
        """
        This constructor sets the maximum loop frequency and loop period.

        :param frequency: int | Loop frequency
        :return: None
        """
        self.__clock = Clock()
        self.set_frequency(frequency)

    def set_frequency(self, frequency: int) -> None:
        """
        This method sets the maximum loop frequency.

        :param frequency: int | Loop frequency
        :return: None
        """
        if frequency <= 0:
            raise ValueError("The frequency must be greater than 0.")
        self.__frequency = frequency
        self.__period = float(1/frequency)

    def slow_loop(self) -> None:
        """
        This method puts the loop to sleep if it is too fast.

        :return: None
        """
        if self.__clock.get_elapsed_time().as_seconds() < self.__period:
            sleep(self.__period - self.__clock.get_elapsed_time().as_seconds())
        self.__clock.restart()
