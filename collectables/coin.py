import arcade
from arcade import PymunkPhysicsEngine
# does not follow scaling rules

coin = 'resources/images/coin.png'

class Coin(arcade.Sprite):
    def __init__(self,physics_engine,stats):
        coin_sheet = arcade.load_spritesheet(coin)
        texture_list = coin_sheet.get_texture_grid(size=(80, 80), columns=8, count=8)
        super().__init__(texture_list[0],scale=0.25)
        self.time_elapsed = 0
        self.cur_texture_index =0
        self.textures = texture_list
        self.physics_engine = physics_engine
        self.stats = stats


    def on_setup(self):
        def player_coin_handler(sprite_a, sprite_b, arbiter, space, data):
            coin_sprite = arbiter.shapes[0]
            coin_sprite = self.physics_engine.get_sprite_for_shape(coin_sprite)
            coin_sprite.remove_from_sprite_lists()
            self.stats.update_coin_number()
            print("Coin")

        self.physics_engine.add_collision_handler(
            "coin",
            "player",
            post_handler=player_coin_handler,
        )
        self.physics_engine.add_sprite(self,
                                       mass=0.1,
                                       damping=0.01,
                                       friction=0.3,
                                       body_type=PymunkPhysicsEngine.DYNAMIC,
                                       collision_type="coin",
                                       elasticity=0.9)
    def apply_force(self,force):
        self.physics_engine.apply_force(self ,force)

    def update(self, delta_time: float = 1/60, *args, **kwargs):
        self.time_elapsed += delta_time
        if self.time_elapsed > 0.3:
            self.set_texture(self.cur_texture_index)
            self.cur_texture_index = (self.cur_texture_index + 1) % len(self.textures)
            self.time_elapsed = 0
