from arcade import PymunkPhysicsEngine

from managers.collision_manager import CollisionManager
from collectables.animation import Animation

class InteractiveItem(Animation):
    def __init__(self, physics_engine, stats, textures, sprite_details):
        super().__init__(textures, sprite_details)
        self.physics_engine = physics_engine
        self.stats = stats
        self.item_type = sprite_details.get("item_type")
        self.collectable = sprite_details.get("collectable", False)
        self.item_lifetime = 0
        self.body_type = sprite_details.get("body_type", PymunkPhysicsEngine.DYNAMIC )
        self.mass = sprite_details.get("mass" , 0.1)
        self.map = map
        self.moment_of_inertia = sprite_details.get("moment_of_inertia", None)
        self.is_physics_setup = False

    def __str__(self):
        return self.item_type

    def apply_force(self,force):
        self.physics_engine.apply_force(self ,force)
    def apply_impulse(self,impulse):
        self.physics_engine.apply_impulse(self ,impulse)

    def on_setup(self):
        if self.is_physics_setup:
            return

        self.physics_engine.add_sprite(self,
                                       mass=self.mass,
                                       damping=0.01,
                                       friction=0.3,
                                       body_type=self.body_type,
                                       moment_of_inertia=self.moment_of_inertia,
                                       collision_type=self.item_type,
                                       elasticity=0.9)
        def item_player_handle(sprite_a, sprite_b, arbiter, space, data):
            if self.collectable:
                item_sprite = arbiter.shapes[0]
                item_sprite = self.physics_engine.get_sprite_for_shape(item_sprite)
                # cursed as fuck it invokes KeyError and then deletes item if no other solution found keep xd
                try:
                    item_sprite.remove_from_sprite_lists()
                except KeyError:
                    pass
            return CollisionManager.handle_effect(self,self.item_type, self.stats)


        self.physics_engine.add_collision_handler(
            self.item_type,
            "player",
            pre_handler=item_player_handle,
        )
        self.is_physics_setup = True

    def remove_from_physics_engine(self):
        self.physics_engine.remove_sprite(self)



    def update(self, delta_time: float = 1/60, *args, **kwargs):
        super().update()
        self.item_lifetime+=1

