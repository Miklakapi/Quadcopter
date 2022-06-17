"""This module handles the communication over I2C between a Raspberry Pi and a MPU-6050 Accelerometer."""

import smbus
import math
from typing import TypeVar


class Accelerometer:
    """
    This class manages the "MPU 6050" accelerometer.
    """

    power_management_1: hex = None
    """Wake up the device"""

    bus: smbus.SMBus = None
    """SMBus module"""

    address: hex = None
    """Device address"""

    def __init__(self, address: hex = 0x68) -> None:
        """
        This constructor wakes up "MPU6050" when it boots up in sleep mode.

        :param address: hex | Device address
        :return None
        """
        self.power_management_1 = 0x6b
        self.bus = smbus.SMBus(1)
        self.address = address
        self.bus.write_byte_data(self.address, self.power_management_1, 0)

    def read_word_2c(self, register: hex) -> float:
        """
        This method read two i2c registers.

        :param register: hex | The first register to read from
        :return: float | Two combined variables
        """
        high = self.bus.read_byte_data(self.address, register)
        low = self.bus.read_byte_data(self.address, register + 1)
        value = (high << 8) + low
        if value >= 0x8000:
            return value - 65536
        return value

    @staticmethod
    def dist(a: float, b: float) -> float:
        """
        This method calculates hypotenuse (Pythagorean theorem).

        :param a: float | First variable
        :param b: float | Second variable
        :return: float | Hypotenuse
        """
        return math.sqrt((a ** 2) + (b ** 2))

    @staticmethod
    def get_x_rotation(x: float, y: float, z: float) -> float:
        """
        This method converts the data into an angle.

        :param x: float | X axis parameters
        :param y: float | Y axis parameters
        :param z: float | Z axis parameters
        :return: float | X axis angle
        """
        return math.degrees(math.atan2(y, Accelerometer.dist(x, z)))

    @staticmethod
    def get_y_rotation(x: float, y: float, z: float) -> float:
        """
        This method converts the data into an angle.

        :param x: float | X axis parameters
        :param y: float | Y axis parameters
        :param z: float | Z axis parameters
        :return: float | Y axis angle
        """
        return math.degrees(math.atan2(x, Accelerometer.dist(y, z)))

    def run(self) -> list:
        """
        This method calculates the device angles.

        :return: list | First index - X axis angle, Second index - Y axis angle
        """
        # Read accelerometer data
        accelerometer_x = self.read_word_2c(0x3b)
        accelerometer_y = self.read_word_2c(0x3d)
        accelerometer_z = self.read_word_2c(0x3f)

        # Scale accelerometer data
        accelerometer_x_scaled = accelerometer_x / 16384.0
        accelerometer_y_scaled = accelerometer_y / 16384.0
        accelerometer_z_scaled = accelerometer_z / 16384.0

        return [
            Accelerometer.get_x_rotation(accelerometer_x_scaled, accelerometer_y_scaled, accelerometer_z_scaled),
            Accelerometer.get_y_rotation(accelerometer_x_scaled, accelerometer_y_scaled, accelerometer_z_scaled)
        ]


MeasurementsFixerObject = TypeVar('MeasurementsFixerObject', bound='MeasurementsFixer')


class MeasurementsFixer:
    """
    This class stores 3 measurements from the accelerometer and calculates the average and rounds it.
    """

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
