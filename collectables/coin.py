from arcade import PymunkPhysicsEngine

from collectables.collectable import Collectable


# does not follow scaling rules
class Coin(Collectable):
    def __init__(self, physics_engine, stats, sprite, sprite_details):
        super().__init__(physics_engine, stats, sprite, sprite_details)

    def on_setup(self):
        def player_coin_handler(sprite_a, sprite_b, arbiter, space, data):
            coin_sprite = arbiter.shapes[0]
            coin_sprite = self.physics_engine.get_sprite_for_shape(coin_sprite)
            coin_sprite.remove_from_sprite_lists()
            self.stats.coins += 1
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
