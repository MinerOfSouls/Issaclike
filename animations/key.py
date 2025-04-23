import arcade
from arcade import PymunkPhysicsEngine
from parameters import *

# does not follow scaling rules
key = 'resources/images/key-white.png'


class Key(arcade.Sprite):
    def __init__(self, physics_engine, stats):
        key_sheet = arcade.load_spritesheet(key)
        texture_list = key_sheet.get_texture_grid(size=(32, 32), columns=12, count=12)
        super().__init__(texture_list[0], scale=0.75)
        self.time_elapsed = 0
        self.cur_texture_index = 0
        self.textures = texture_list
        self.physics_engine = physics_engine
        self.stats = stats

    def on_setup(self):
        def player_key_handler(sprite_a, sprite_b, arbiter, space, data):
            key_sprite = arbiter.shapes[0]
            key_sprite = self.physics_engine.get_sprite_for_shape(key_sprite)
            key_sprite.remove_from_sprite_lists()
            self.stats.keys +=1
            print("Key")

        self.physics_engine.add_collision_handler(
            "key",
            "player",
            post_handler=player_key_handler,
        )
        self.physics_engine.add_sprite(self,
                                       mass=0.1,
                                       damping=0.01,
                                       friction=0.3,
                                       body_type=PymunkPhysicsEngine.DYNAMIC,
                                       collision_type="key",
                                       elasticity=0.9)

    def apply_force(self,force):
        self.physics_engine.apply_force(self ,force)


    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        self.time_elapsed += delta_time
        if self.time_elapsed > 0.3:
            self.set_texture(self.cur_texture_index)
            self.cur_texture_index = (self.cur_texture_index + 1) % len(self.textures)
            self.time_elapsed = 0
