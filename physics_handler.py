class PhysicsHandler:
    def __init__(self,physics_engine,stats):
        self.physics_engine = physics_engine
        self.stats = stats

    def on_setup(self):
        def player_coin_handler(sprite_a, sprite_b, arbiter, space, data):
            coin_sprite = arbiter.shapes[0]
            coin_sprite = self.physics_engine.get_sprite_for_shape(coin_sprite)
            coin_sprite.remove_from_sprite_lists()
            self.stats.coins +=1
            print("Coin")

        self.physics_engine.add_collision_handler(
            "player",
            "coin",
            post_handler=player_coin_handler,
        )
