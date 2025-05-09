import arcade
from arcade import PymunkPhysicsEngine
from random import randint

from collectables.interactive_item import InteractiveItem

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
                match rand:
                    case 0:
                        coin = self.pickup_factory.spawn_coin(spawn_x, spawn_y)
                        coin.apply_force((x_accel, y_accel))
                    case 1:
                        key = self.pickup_factory.spawn_key(spawn_x, spawn_y)
                        key.apply_force((x_accel, y_accel))
                    case 2:
                        bomb = self.pickup_factory.spawn_bomb(spawn_x, spawn_y)
                        bomb.apply_force((x_accel, y_accel))
            self.opened = True

    def on_setup(self):
        def player_chest_handler(sprite_a, sprite_b, arbiter, space, data):
            if self.stats.keys >0:
                self.set_texture(1)
                self.spawn_chest_contents()
                self.stats.keys -= 1

        self.physics_engine.add_collision_handler(
            "chest",
            "player",
            post_handler=player_chest_handler,
        )
        self.physics_engine.add_sprite(self,
                                       mass=1,
                                       damping=0.01,
                                       friction=1,
                                       body_type=PymunkPhysicsEngine.STATIC,
                                       moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="chest",
                                       elasticity=1)

    def update(self, delta_time: float = 1/60, *args, **kwargs):
        pass