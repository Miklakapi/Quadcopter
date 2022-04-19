"""drone.py: Drone management module"""

__name__ = "Drone"
__author__ = "Kacper Miklaszewski"
__license__ = "MIT"
__version__ = "1.0.0"
__status__ = "Production"

import RPi.GPIO as GPIO
import threading
from typing import List
from time import sleep
import time_
from drone_action import DroneRotation, DroneSlope
from accelerometer import Accelerometer

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class Drone(threading.Thread):
    """
    A class that represents a drone

    This class manages the drone

    :param motor_list: List[RPi.GPIO.PWM] | List of all motors
    :param power_difference: List[float] | List of motors power differentials
    :param __main_power: float | Represents motors main power
    :param led_list: List[RPi.GPIO.PWM] | List of all led
    :param slope: DroneSlope | Represents the drone slope
    :param rotation: DroneRotation | Represents the drone rotation
    :param frequency: time_.LoopRate | Maximum loop frequency
    :param lock: threading.Lock | Variable for synchronizing threads
    """

    motor_list: List[GPIO.PWM] = []
    power_difference: List[float] = []
    __main_power: float = None
    led_list: List[GPIO.PWM] = []
    slope: DroneSlope = None
    rotation: DroneRotation = None
    frequency: time_.LoopRate = None
    lock: threading.Lock = None

    def __init__(self, motor_list: List[int], led_list: List[int], frequency: int) -> None:
        """
        This constructor sets GPIO pin value
        :param motor_list: List[int] | List of all motors
        :param led_list: List[int] | List of all leds
        :param frequency: int | Maximum loop frequency
        :return: None
        """
        for x in range(4):
            GPIO.setup(motor_list[x], GPIO.OUT)
            GPIO.setup(led_list[x], GPIO.OUT)

            self.motor_list.append(GPIO.PWM(motor_list[x], 50))
            self.led_list.append(GPIO.PWM(led_list[x], 50))

            self.power_difference.append(0)
        self.__main_power = 0
        self.slope = DroneSlope.Stay
        self.rotation = DroneRotation.Stay
        self.frequency = time_.LoopRate(frequency)
        self.lock = threading.Lock()
        self.__start_pwm()
        threading.Thread.__init__(self)

    def set_motor_power(self, power: float) -> None:
        """
        This method sets motors power
        :param power: float | PWM of motors pins
        :return: None
        """
        self.lock.acquire()
        self.__main_power = power

        if power < 5.5:
            for x in range(4):
                self.power_difference[x] = 0
        elif power + max(self.power_difference) > 10:
            regulation: float = (power + max(self.power_difference)) - 10
            for x in range(4):
                self.power_difference[x] -= regulation
        elif power + min(self.power_difference) < 5.5:
            regulation: float = 5.5 - (power + min(self.power_difference))
            for x in range(4):
                self.power_difference[x] += regulation

        for x in range(4):
            self.motor_list[x].ChangeDutyCycle(power + self.power_difference[x])
        self.lock.release()

    def set_rotation(self, rotation: DroneRotation, slope: bool) -> None:
        """
        This method rotates the drone
        :param rotation: DroneRotation | Direction of rotation
        :param slope: bool | Sets whether the function should clear the slope
        :return: None
        """
        if slope:
            self.set_slope(DroneSlope.Stay, False)

        if rotation != self.rotation:
            regulation = 0.15

            self.lock.acquire()
            self.slope = DroneSlope.Stay

            difference: int = int(rotation) - int(self.rotation)
            self.power_difference[0] += (difference * -regulation)
            self.power_difference[1] += (difference * regulation)
            self.power_difference[2] += (difference * regulation)
            self.power_difference[3] += (difference * -regulation)

            if self.__main_power + max(self.power_difference) > 10:
                regulation: float = (self.__main_power + max(self.power_difference)) - 10
                for x in range(4):
                    self.power_difference[x] -= regulation
            elif self.__main_power + min(self.power_difference) < 5.5:
                regulation: float = 5.5 - (self.__main_power + min(self.power_difference))
                for x in range(4):
                    self.power_difference[x] += regulation

            for x in range(4):
                self.motor_list[x].ChangeDutyCycle(self.__main_power + self.power_difference[x])

            self.lock.release()
            self.rotation = rotation

    def set_slope(self, slope: DroneSlope, rotation: bool) -> None:
        """
        This method sets the drone slope
        :param slope: DroneSlope | Represents the drone slope
        :param rotation: bool | Sets whether the function should clear the rotation
        :return: None
        """
        if rotation:
            self.set_rotation(DroneRotation.Stay, False)

        if slope == self.slope:
            regulation = 0.125

            self.lock.acquire()

            if self.slope == DroneSlope.Forward:
                self.power_difference[0] += regulation
                self.power_difference[1] += regulation
                self.power_difference[2] -= regulation
                self.power_difference[3] -= regulation
            elif self.slope == DroneSlope.Backward:
                self.power_difference[0] -= regulation
                self.power_difference[1] -= regulation
                self.power_difference[2] += regulation
                self.power_difference[3] += regulation
            elif self.slope == DroneSlope.Left:
                self.power_difference[0] += regulation
                self.power_difference[1] -= regulation
                self.power_difference[2] += regulation
                self.power_difference[3] -= regulation
            elif self.slope == DroneSlope.Right:
                self.power_difference[0] -= regulation
                self.power_difference[1] += regulation
                self.power_difference[2] -= regulation
                self.power_difference[3] += regulation

            if slope == DroneSlope.Forward:
                self.power_difference[0] -= regulation
                self.power_difference[1] -= regulation
                self.power_difference[2] += regulation
                self.power_difference[3] += regulation
            elif slope == DroneSlope.Backward:
                self.power_difference[0] += regulation
                self.power_difference[1] += regulation
                self.power_difference[2] -= regulation
                self.power_difference[3] -= regulation
            elif slope == DroneSlope.Left:
                self.power_difference[0] -= regulation
                self.power_difference[1] += regulation
                self.power_difference[2] -= regulation
                self.power_difference[3] += regulation
            elif slope == DroneSlope.Right:
                self.power_difference[0] += regulation
                self.power_difference[1] -= regulation
                self.power_difference[2] += regulation
                self.power_difference[3] -= regulation

            self.slope = slope
            self.lock.release()

    def run(self) -> None:
        """
        This method controls the LEDs and the accelerometer
        :return: None
        """
        # Led variable
        clock_1 = time_.Clock()
        flag_1 = True

        # Gyroscope variable
        clock_2 = time_.Clock()
        accelerometer = Accelerometer()

        while True:
            # Leds
            if clock_1.get_elapsed_time().as_seconds() >= 1:
                if flag_1:
                    self.led_list[0].ChangeDutyCycle(100)
                    self.led_list[1].ChangeDutyCycle(0)
                    self.led_list[2].ChangeDutyCycle(0)
                    self.led_list[3].ChangeDutyCycle(100)
                    flag_1 = False
                else:
                    self.led_list[0].ChangeDutyCycle(0)
                    self.led_list[1].ChangeDutyCycle(100)
                    self.led_list[2].ChangeDutyCycle(100)
                    self.led_list[3].ChangeDutyCycle(0)
                    flag_1 = True
                clock_1.restart()
            # Gyroscope
            if clock_2.get_elapsed_time().as_seconds() >= 0.1:
                data = accelerometer.run()
                x_angle = data[0]
                y_angle = data[1]
                self.__angle(x_angle, y_angle)
            # Frequency
            self.frequency.slow()

    def __start_pwm(self) -> None:
        """
        This method turns the motors on and tests them
        :return: None
        """
        # Turn the motors on
        for x in range(4):
            self.motor_list[x].start(4)
            self.led_list[x].start(0)
        self.__main_power = 4
        sleep(7)
        # Test the leds and motors
        for x in range(4):
            self.motor_list[x].ChangeDutyCycle(5.7)
            self.led_list[x].ChangeDutyCycle(100)
            sleep(2)
            self.motor_list[x].ChangeDutyCycle(5)
            self.led_list[x].ChangeDutyCycle(0)
            sleep(0.3)
        self.__main_power = 5

#############################
    def __angle(self, x_angle: float, y_angle: float) -> None:
        """
        This method sets the drone slope
        :param x_angle: float | Actual angle
        :param y_angle: float | Actual angle
        :return: None
        """
        regulation: float = 0.05
        self.lock.acquire()

        if self.__main_power < 5.5:
            for x in range(4):
                self.power_difference[x] = 0
            self.lock.release()
            return

        x_range: List[int] = [0, 0]
        y_range: List[int] = [0, 0]

        if self.slope == DroneSlope.Stay:
            x_range[0] = 4
            x_range[1] = -4
            y_range[0] = 4
            y_range[1] = -4
        elif self.slope == DroneSlope.Right:
            x_range[0] = 19
            x_range[1] = 11
            y_range[0] = 4
            y_range[1] = -4
        elif self.slope == DroneSlope.Left:
            x_range[0] = -11
            x_range[1] = -19
            y_range[0] = 4
            y_range[1] = -4
        elif self.slope == DroneSlope.Forward:
            x_range[0] = 4
            x_range[1] = -4
            y_range[0] = 19
            y_range[1] = 11
        elif self.slope == DroneSlope.Backward:
            x_range[0] = 4
            x_range[1] = -4
            y_range[0] = -11
            y_range[1] = -19

        # X
        if x_angle > x_range[0]:
            self.power_difference[0] -= regulation
            self.power_difference[1] += regulation
            self.power_difference[2] -= regulation
            self.power_difference[3] += regulation
        elif x_angle < x_range[1]:
            self.power_difference[0] += regulation
            self.power_difference[1] -= regulation
            self.power_difference[2] += regulation
            self.power_difference[3] -= regulation
        # Y
        if y_angle > y_range[0]:
            self.power_difference[0] += regulation
            self.power_difference[1] += regulation
            self.power_difference[2] -= regulation
            self.power_difference[3] -= regulation
        elif y_angle < y_range[1]:
            self.power_difference[0] -= regulation
            self.power_difference[1] -= regulation
            self.power_difference[2] += regulation
            self.power_difference[3] += regulation

        if self.__main_power + max(self.power_difference) > 10:
            regulation2: float = (self.__main_power + max(self.power_difference)) - 10
            for x in range(4):
                self.power_difference[x] -= regulation2
        elif self.__main_power + min(self.power_difference) < 5.5:
            regulation2: float = 5.5 - (self.__main_power + min(self.power_difference))
            for x in range(4):
                self.power_difference[x] += regulation2

        # print('{}'.format(self.power_difference))
        print('x: {}, y: {}'.format(x_angle, y_angle))

        for x in range(4):
           # self.motor_list[x].ChangeDutyCycle(self.__main_power + self.power_difference[x])

           print('{}'.format(self.__main_power + self.power_difference[x]))

        self.lock.release()

    def __del__(self) -> None:
        """
        This deconstructor clears GPIO pin value
        :return: None
        """
        for x in self.motor_list:
            x.ChangeDustyCycle(5)
        sleep(0.5)
        for x in range(4):
            self.motor_list[x].stop()
            self.led_list[x].stop()
        GPIO.cleanup()
