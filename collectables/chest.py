import random

from random import randint

from arcade import PymunkPhysicsEngine

from characters.stats import Stats
from collectables.base.interactive_item import InteractiveItem
from collectables.pickup_factory import PickupType, PickupFactory


class Chest(InteractiveItem):
    def __init__(self, physics_engine: PymunkPhysicsEngine, pickup_factory: PickupFactory, stats: Stats, texture_list,
                 sprite_details: dict):
        super().__init__(physics_engine, stats, texture_list, sprite_details)
        self.pickup_factory = pickup_factory
        self.opened = False

    def spawn_chest_contents(self) -> None:
        if not self.opened:
            num = randint(0, 10)
            for i in range(num):
                x_offset = randint(-50, 50)
                y_offset = randint(0, 50)
                spawn_x = int(self.center_x + x_offset)
                spawn_y = int(self.center_y + y_offset)

                # Random acceleration values
                x_accel = randint(-1000, 1000)
                y_accel = randint(400, 1600)
                item_type = random.choice(list(PickupType))
                item = self.pickup_factory.create_pickup(item_type, spawn_x, spawn_y)
                item.apply_force((x_accel, y_accel))
            self.opened = True
