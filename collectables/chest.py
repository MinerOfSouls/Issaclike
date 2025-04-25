import arcade
from arcade import PymunkPhysicsEngine
from random import randint


# does not follow scaling rules
chest = 'resources/images/chest-ss.png'


class Chest(arcade.Sprite):
    def __init__(self, physics_engine,pickup_factory, stats):
        chest_sheet = arcade.load_spritesheet(chest)
        texture_list = chest_sheet.get_texture_grid(size=(48, 32), columns=4, count=4)
        super().__init__(texture_list[0], scale=2)
        self.pickup_factory = pickup_factory
        self.time_elapsed = 0
        self.cur_texture_index = 0
        self.textures = texture_list
        self.physics_engine = physics_engine
        self.stats = stats
        self.opened = False

    def spawn_chest_contents(self):
        if not self.opened:
            num = randint(0, 10)
            for i in range(num):
                rand = randint(0, 2)
                # Random position near the chest
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
                        # todo make a bomb
                        pass
            self.opened = True
    def on_setup(self):
        def player_chest_handler(sprite_a, sprite_b, arbiter, space, data):
            self.set_texture(1)
            self.spawn_chest_contents()
            # self.stats.chests +=1
            print("chest")

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
