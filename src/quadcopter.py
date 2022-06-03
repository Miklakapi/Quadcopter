#!/usr/bin/env python

"""123"""

import RPi.GPIO as GPIO
from time import sleep


class Quadcopter:
    """
    123
    """

    __motor_list = None
    """123"""

    __main_power = None
    """123"""

    __led_list = None
    """123"""

    def __init__(self):
        pass

    def set_main_power(self):
        pass

    def set_action(self):
        pass

    def run(self):
        pass

    def __start_pwm(self) -> None:
        """
        This method turns on and tests the motors and LEDs.

        :return: None
        """
        for x in self.__motor_list:
            x.start(4)
        for x in self.__led_list:
            x.start(0)
        self.__main_power = 4
        sleep(5)
        for x in self.__motor_list:
            x.ChangeDutyCycle(5.7)
            x.ChangeDutyCycle(100)
            sleep(2)
            x.ChangeDutyCycle(5)
            x.ChangeDutyCycle(0)
            sleep(0.3)
        self.__main_power = 5

    def __del__(self) -> None:
        """
        This destructor clears GPIO pin value.

        :return: None
        """
        for x in self.__motor_list:
            x.ChangeDustyCycle(5)
        sleep(0.5)
        for x in range(4):
            self.__motor_list[x].stop()
            self.__led_list[x].stop()
        GPIO.cleanup()
