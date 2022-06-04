#!/usr/bin/env python

"""Module to control quadcopter"""

from xmlrpc.client import Boolean
import RPi.GPIO as GPIO
from time import sleep

from file_reader import FileReader


class Quadcopter:
    """
    Class that manage the quacopter 
    """

    motor_list = {}
    """Dictionary of motors"""

    led_list = {}
    """Dictionary of leds"""

    main_power = None
    """Main power of motors"""

    def __init__(self) -> None:
        """
        This constructor reads the settings from the file and starts the quadcopter.
        """
        reader = FileReader('motors', '../data/motor_pins.json')
        reader.add_file('leds', '../data/led_pins.json')

        motors = reader.get_data('motors')
        leds = reader.get_data('leds')

        for x in motors:
            GPIO.setup(motors[x], GPIO.OUT, initial=GPIO.LOW)
            self.motor_list.update({
                x: {
                    'pin': motors[x],
                    'gpio': GPIO.PWM(motors[x], 50),
                    'extra_power': 0
                }
            })

        for x in leds:
            GPIO.setup(leds[x], GPIO.OUT, initial=GPIO.LOW)
            self.led_list.update({
                x: {
                    'pin': leds[x],
                    'active': False
                }
            })

        self.start_pwm()

    def set_main_power(self, main_power: float) -> None:
        """
        This method determines the main power of the quadcopter.

        :param main_power: float | Power
        :return: None
        """
        if main_power < 0 or main_power > 10:
            raise Exception('Wrong power')
        self.main_power = main_power

        for x in self.motor_list.values():
            x['gpio'].ChangeDutyCycle(main_power + x['extra_power'])

    def set_action(self):
        pass

    def run(self):
        pass

    def start_pwm(self) -> None:
        """
        This method turns on and tests the motors and LEDs.

        :return: None
        """
        for x in self.motor_list:
            self.motor_list[x]['gpio'].start(4)

        sleep(5)
        for x in self.motor_list:
            self.motor_list[x]['gpio'].ChangeDutyCycle(5.7)
            self.switch_led(self.led_list[x])
            sleep(2)
            self.motor_list[x]['gpio'].ChangeDutyCycle(5)
        self.main_power = 5

    def switch_led(led: dict) -> Boolean:
        """
        This method changes the state of the led.
        
        :param led: dict | Led
        :return: Boolean | Led state
        """
        led['active'] = not led['active']
        GPIO.setup(led['pin'], led['active'])
        return led['active']

    def __del__(self) -> None:
        """
        This destructor clears GPIO pin value.

        :return: None
        """
        for x in self.motor_list.values():
            x['gpio'].ChangeDustyCycle(5)
        sleep(0.5)
        for x in self.motor_list.values():
            x.stop()
        for x in self.led_list.values():
            GPIO.setup(x['pin'], 0)
        GPIO.cleanup()
