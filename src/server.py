from bottle import route, run
from drone import Drone
from drone_action import DroneRotation, DroneSlope

# Creating an object (Drone) and turning on motors and testing them
quadcopter = Drone([20, 12, 21, 16], [6, 26, 13, 19], 30)

# Setting Drone as daemon
quadcopter.setDaemon(True)
# Setting Drone as the second thread
quadcopter.start()


@route('/power/<power:float>')
def motors(power: float) -> None:
    """
    This function sets the motors power
    :link: http://192.168.0.202:8000/power/(value: float)
    :param power: float | Motors power
    :return: None
    """
    quadcopter.set_motor_power(power)


@route('/direction/<side:int>')
def slope(side: int) -> None:
    """
    This function sets the drone slope
    :link: http://192.168.0.202:8000/direction/(side: int)
    :param side: int
        0 - Stay
        1 - Forward
        2 - Backward
        3 - Left
        4 - Right
    :return: None
    """
    quadcopter.set_slope(DroneSlope(side), True)


@route('/rotation/<direction:int>')
def rotation(direction: int) -> None:
    """
    This function rotates the drone
    :link: http://192.168.0.202:8000/rotation/(direction: int)
    :param direction: int
        0 - Left
        1 - Stay
        2 - Right
    :return: None
    """
    quadcopter.set_rotation(DroneRotation(direction), True)


run(host='192.168.0.202', port=8000)
