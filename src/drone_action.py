"""drone_action.py: Drone actions (Enum) module"""

__name__ = "Drone Actions"
__author__ = "Kacper Miklaszewski"
__license__ = "MIT"
__version__ = "1.0.0"
__status__ = "Production"

from enum import Enum, IntEnum


class DroneRotation(IntEnum):
    """
    A class that represents drone rotation
    """
    Left = 0
    Stay = 1
    Right = 2


class DroneSlope(Enum):
    """
    A class that represents drone slope
    """
    Stay = 0
    Forward = 1
    Backward = 2
    Left = 3
    Right = 4
