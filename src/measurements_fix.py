#!/usr/bin/env python

"""This module stores 3 measurements from the accelerometer and calculates the average and rounds it."""

from typing import TypeVar

MeasurementsFixerObject = TypeVar('MeasurementsFixerObject', bound='MeasurementsFixer')


class MeasurementsFixer:

    measurements_array: list = None
    """Stores the history of measurements"""

    round_position: int = None
    """Holds the position to which the class will round numbers"""

    def __init__(self, round_position: int = 0) -> None:
        """
        This constructor sets the measurement history and round_position.
        
        :param round_position: int | Position to which the class will round numbers
        :return: None
        """
        self.measurements_array = [[0, 0], [0, 0], [0, 0]]
        self.set_round(round_position)

    def set_round(self, round_position: int) -> MeasurementsFixerObject:
        """
        Sets position to which the class will round numbers.

        :param round_position: int | Position to which the class will round numbers
        :return: self
        """
        if round_position < -1:
            raise ValueError('Wrong round_position. ' + str(round_position) + ' should be greater than -1.')
        self.round_position = round_position
        return self

    def add_measurement(self, measurement: list) -> MeasurementsFixerObject:
        """
        Adds data to the FIFO.

        :param measurement: list | Data from accelerometer
        :return: self
        """
        self.measurements_array.pop(0)
        self.measurements_array.append(measurement)
        return self

    def get_all_measurements(self) -> list:
        """
        Returns a Copy of the measurement history.

        :return: list | Copy of the measurement history
        """
        return self.measurements_array.copy()

    def get_fixed_measurement(self) -> list:
        """
        Returns the corrected measurement history data.

        :return: list | Fixed measurement history data
        """
        return [
            round((
                    (
                            self.measurements_array[0][0] +
                            self.measurements_array[1][0] +
                            self.measurements_array[2][0]
                    ) / 3), self.round_position),
            round((
                    (
                            self.measurements_array[0][1] +
                            self.measurements_array[1][1] +
                            self.measurements_array[2][1]
                    ) / 3), self.round_position)
        ]
