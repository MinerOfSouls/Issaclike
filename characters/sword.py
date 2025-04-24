import arcade
from arcade import PymunkPhysicsEngine

# does not follow scaling rules
sword = 'resources/images/sword.png'

class Sword(arcade.Sprite):
    def __init__(self, physics_engine, stats):
        sword_sheet = arcade.load_spritesheet(sword)
        texture_list = sword_sheet.get_texture_grid(size=(32, 32), columns=11, count=11)
        super().__init__(texture_list[0], scale=1.5)
        self.time_elapsed = 0
        self.cur_texture_index = 0
        self.textures = texture_list
        self.physics_engine = physics_engine
        self.stats = stats

        self.charge_time = 30
        self.charging = 0
        self.held = True
        self.returning = False

    def on_setup(self):
        def enemy_sword_handler(sprite_a, sprite_b, arbiter, space, data):
            sword_sprite = arbiter.shapes[0]
            sword_sprite = self.physics_engine.get_sprite_for_shape(sword_sprite)
            sword_sprite.remove_from_sprite_lists()
            print("sword")

        self.physics_engine.add_collision_handler(
            "sword",
            "enemy",
            post_handler=enemy_sword_handler,
        )

        self.physics_engine.add_sprite(self,
                                       mass=0.1,
                                       damping=0.01,
                                       friction=0.3,
                                       moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
                                       body_type=PymunkPhysicsEngine.DYNAMIC,
                                       collision_type="sword",
                                       elasticity=0.9)

    def apply_impulse(self,force):
        self.physics_engine.apply_impulse(self ,force)

    def apply_force(self,impulse):
        self.physics_engine.apply_force(self ,impulse)

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        if self.charging >= self.charge_time:
            self.time_elapsed += delta_time
            if self.time_elapsed > 0.3:
                self.set_texture(self.cur_texture_index)
                self.cur_texture_index = (self.cur_texture_index + 1) % len(self.textures)
                self.time_elapsed = 0
