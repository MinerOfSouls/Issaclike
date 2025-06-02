from enum import Enum, auto


class PickupType(Enum):
    COIN = auto()
    KEY = auto()
    BOMB = auto()
    HEALTH_POTION = auto()
    DAMAGE_POTION = auto()
    RANGE_POTION = auto()
    SPEED_POTION = auto()
