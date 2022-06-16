"""Module to control quadcopter"""

import RPi.GPIO as GPIO
from time import sleep
from enum import Enum

from file_reader import FileReader
from accelerometer import Accelerometer
from measurements_fix import MeasurementsFixer
from timers import Clock

#       ┌────┐y +┌────┐
#       │ 01 │   │ 02 │
#       └────┘   └────┘
#             \ /
#       x+     X     x-
#             / \
#       ┌────┐   ┌────┐
#       │ 03 │   │ 04 │
#       └────┘y -└────┘


class Quadcopter:
    """
    Class that manage the quacopter 
    """

    class Action(Enum):
        STAY = 0
        FORWARD = 1
        ROTATE_LEFT = 2
        LEFT = 3
        ROTATE_RIGHT = 4
        RIGHT = 5
        BACKWARD = 6

    motor_dict: dict = {}
    """Dictionary of motors"""

    led_dict: dict = {}
    """Dictionary of leds"""

    main_power: float = None
    """Main power of motors"""

    accelerometer: Accelerometer = None
    """Accelerometer"""

    measure_fixer: MeasurementsFixer = None
    """Measure fixer"""

    led_clock: Clock = None
    """Led clock"""

    action: Action = None
    """Quadcopter action"""

    x_angle_range: list = []
    """X axis range"""

    x_delta_power: float = 0
    """The difference in engine power on the x axis"""

    y_angle_range: list = []
    """Y axis range"""

    y_delta_power: float = 0
    """The difference in engine power on the y axis"""

    CONST_POWER_JUMP: float = 0.08
    """The value of the engine power jump if the flight is unstable"""

    CONST_MAX_DELTA: float = 2
    """Maximum delta of power difference"""

    CONST_MAX_POWER: float = 10.0
    """Max motor power"""

    CONST_MIN_POWER: float = 5.0
    """Min motor power"""

    def __init__(self) -> None:
        """
        This constructor reads the settings from the file and starts the quadcopter.
        """
        reader = FileReader('motors', '../data/motor_pins.json')
        reader.add_file('leds', '../data/led_pins.json')

        motors = reader.get_data('motors')
        leds = reader.get_data('leds')

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        for x in motors:
            GPIO.setup(motors[x], GPIO.OUT, initial=GPIO.LOW)
            self.motor_dict.update({
                x: {
                    'pin': motors[x],
                    'gpio': GPIO.PWM(motors[x], 50),
                    'extra_power': 0
                }
            })

        for x in leds:
            GPIO.setup(leds[x], GPIO.OUT, initial=GPIO.LOW)
            self.led_dict.update({
                x: {
                    'pin': leds[x],
                    'active': False
                }
            })

        self.accelerometer = Accelerometer()
        self.measure_fixer = MeasurementsFixer()
        self.led_clock = Clock()

        self.set_action(self.Action(0))

        self.start_pwm()
        self.start_leds()

    def set_main_power(self, main_power: float) -> None:
        """
        This method determines the main power of the quadcopter.

        :param main_power: float | Power
        :return: None
        """
        if main_power < 0 or main_power > 10:
            raise Exception('Wrong power')
        self.main_power = main_power

    def set_powers(self) -> None:
        """
        This method sets the power on each individual motor.

        :return: None
        """
        for x in self.motor_dict.values():
            x['gpio'].ChangeDutyCycle(self.main_power + x['extra_power'])

    def set_action(self, action: Action) -> None:
        """
        This method sets the activity of the quadcopter and changes the range of angles.
        
        :param action: Action | Drone action
        :return: None
        """
        x_angle_range = [-1, 1]
        y_angle_range = [-1, 1]
        if action == self.Action.FORWARD:
            x_angle_range = [18, 22]
        elif action == self.Action.BACKWARD:
            x_angle_range = [-22, -18]
        elif action == self.Action.LEFT:
            y_angle_range = [-22, -18]
        elif action == self.Action.RIGHT:
            y_angle_range = [18, 22]

        self.action = action
        self.x_angle_range = x_angle_range
        self.y_angle_range = y_angle_range

    def run(self) -> None:
        """
        This method manages the quadcopter using data from the accelerometer.

        :return: None
        """
        if self.led_clock.get_elapsed_time().as_seconds() >= 2:
            for x in self.led_dict.values():
                self.switch_led(x)
            self.led_clock.restart()
        
        for i in range(3):
            self.measure_fixer.add_measurement(self.accelerometer.run())
            sleep(0.06)
        angle = self.measure_fixer.get_fixed_measurement()

        if angle[0] < self.x_angle_range[0]:
            if self.x_delta_power <= self.CONST_MAX_DELTA - self.CONST_POWER_JUMP:
                self.x_delta_power += self.CONST_POWER_JUMP
        elif angle[0] > self.x_angle_range[1]:
            if self.x_delta_power >= -self.CONST_MAX_DELTA + self.CONST_POWER_JUMP:
                self.x_delta_power -= 0.08

        if angle[1] < self.y_angle_range[0]:
            if self.y_delta_power <= self.CONST_MAX_DELTA - self.CONST_POWER_JUMP:
                self.y_delta_power += self.CONST_POWER_JUMP
        elif angle[1] > self.y_angle_range[1]:
            if self.y_delta_power >= -self.CONST_MAX_DELTA + self.CONST_POWER_JUMP:
                self.y_delta_power -= self.CONST_POWER_JUMP
        
        self.distribute_power()
        self.set_powers()

    def distribute_power(self) -> None:
        """
        This method distributes power between the motors based on a variable delta.

        :return: None
        """
        power_per_engine_left = self.x_delta_power / 2
        power_per_engine_right = -power_per_engine_left

        self.motor_dict['frontLeft']['extra_power'] = power_per_engine_left
        self.motor_dict['backLeft']['extra_power'] = power_per_engine_left
        self.motor_dict['frontRight']['extra_power'] = power_per_engine_right
        self.motor_dict['backRight']['extra_power'] = power_per_engine_right

        power_per_engine_front = self.y_delta_power / 2
        power_per_engine_back = -power_per_engine_front

        self.motor_dict['frontRight']['extra_power'] += power_per_engine_front
        self.motor_dict['frontLeft']['extra_power'] += power_per_engine_front
        self.motor_dict['backRight']['extra_power'] += power_per_engine_back
        self.motor_dict['backLeft']['extra_power'] += power_per_engine_back

        powers = [
            self.get_calculated_power('frontRight'),
            self.get_calculated_power('frontLeft'),
            self.get_calculated_power('backRight'),
            self.get_calculated_power('backLeft')
        ]

        max_power = max(powers)
        min_power = min(powers)
        if max_power > self.CONST_MAX_POWER:
            power_reduction = max_power - 10
            for motor in self.motor_dict.values():
                motor['extra_power'] -= power_reduction
        elif min_power < self.CONST_MIN_POWER:
            extra_power = self.CONST_MIN_POWER - min_power
            for motor in self.motor_dict.values():
                motor['extra_power'] += extra_power

    def get_calculated_power(self, motor_name) -> float:
        """
        This method calculates the motor power and returns it.
        
        :return: float | Calculated_power
        """
        return self.main_power + self.motor_dict[motor_name]['extra_power']

    def start_pwm(self) -> None:
        """
        This method turns on and tests the motors and LEDs.

        :return: None
        """
        for x in self.motor_dict.values():
            x['gpio'].start(4)

        sleep(5)
        for x in self.motor_dict:
            self.motor_dict[x]['gpio'].ChangeDutyCycle(5.7)
            self.set_led(self.led_dict[x], True)
            sleep(2)
            self.motor_dict[x]['gpio'].ChangeDutyCycle(5)
            self.set_led(self.led_dict[x], False)
        self.main_power = 5
    
    def start_leds(self) -> None:
        """
        This method informs you that the drone is ready by means of LEDs. It also sets the appropriate state of the LEDs and resets the clock.

        :return: None
        """
        for x in range(3):
            for x in self.led_dict.values():
                self.set_led(x, True)
            sleep(0.3)
            for x in self.led_dict.values():
                self.set_led(x, False)

        self.set_led(self.led_dict['frontLeft'], True)
        self.set_led(self.led_dict['backRight'], True)

    def set_led(self, led: dict, active: bool) -> None:
        """
        This method set led state

        :param led: dict | Led
        :param active: bool | Led status
        :return: None
        """
        GPIO.setup(led['pin'], active)
        led['active'] = active

    def switch_led(self, led: dict) -> bool:
        """
        This method changes the state of the led.
        
        :param led: dict | Led
        :return: bool | Led state
        """
        led['active'] = not led['active']
        GPIO.setup(led['pin'], led['active'])
        return led['active']

    def get_powers(self) -> dict:
        """
        This method returns the power of the motors to generate a visualization for testing purposes.

        :return: dict | Dictionary of motors power
        """
        powers = {}
        print(self.main_power)
        for loop_index, x in enumerate(self.motor_dict.values()):
            powers.update({
                loop_index: self.main_power + x['extra_power']
            })
        return powers

    def __del__(self) -> None:
        """
        This destructor clears GPIO pin value.

        :return: None
        """
        for x in self.motor_dict.values():
            x['gpio'].ChangeDutyCycle(5)
        sleep(0.5)
        for x in self.motor_dict.values():
            x['gpio'].stop()
        for x in self.led_dict.values():
            GPIO.setup(x['pin'], 0)
        GPIO.cleanup()
