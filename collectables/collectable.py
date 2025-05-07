import arcade
from arcade import PymunkPhysicsEngine

from collectables.EffectHandler import EffectHandler
from collectables.animation import Animation

class Collectable(Animation):
    def __init__(self, physics_engine, stats, sprite, sprite_details):
        super().__init__(sprite, sprite_details)
        self.physics_engine = physics_engine
        self.stats = stats
        self.item_type = sprite_details.get("item_type")
        self.collectable = sprite_details.get("collectable")

    def apply_force(self,force):
        self.physics_engine.apply_force(self ,force)

    def on_setup(self):
        self.physics_engine.add_sprite(self,
                                       mass=0.1,
                                       damping=0.01,
                                       friction=0.3,
                                       body_type=PymunkPhysicsEngine.DYNAMIC,
                                       collision_type=self.item_type,
                                       elasticity=0.9)

        def item_player_handle(sprite_a, sprite_b, arbiter, space, data):
            if self.collectable:
                item_sprite = arbiter.shapes[0]
                item_sprite = self.physics_engine.get_sprite_for_shape(item_sprite)
                item_sprite.remove_from_sprite_lists()
            print(self.item_type)
            return EffectHandler.handle_effect(self.item_type , self.stats)


        self.physics_engine.add_collision_handler(
            self.item_type,
            "player",
            pre_handler=item_player_handle,
        )