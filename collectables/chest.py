import random

import arcade
from arcade import PymunkPhysicsEngine
from random import randint

from collectables.interactive_item import InteractiveItem
from collectables.pickup_factory import PickupType


# does not follow scaling rules
class Chest(InteractiveItem):
    def __init__(self, physics_engine, pickup_factory, stats, sprite_url, sprite_details):
        super().__init__(physics_engine, stats, sprite_url, sprite_details)
        self.pickup_factory = pickup_factory
        self.opened = False

    def spawn_chest_contents(self):
        if not self.opened:
            num = randint(0, 10)
            for i in range(num):
                rand = randint(0, 2)
                x_offset = randint(-50, 50)
                y_offset = randint(0, 50)
                spawn_x = self.center_x + x_offset
                spawn_y = self.center_y + y_offset

                # Random acceleration values
                x_accel = randint(-1000, 1000)
                y_accel = randint(400, 1600)
                item_type = random.choice(list(PickupType))
                item = self.pickup_factory.create_pickup(item_type, spawn_x, spawn_y)
                item.apply_force((x_accel, y_accel))
            self.opened = True

