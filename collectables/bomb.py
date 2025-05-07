from arcade import PymunkPhysicsEngine

from collectables.animation import Animation
from collectables.collectable import Collectable
from pickup_factory import PickupFactory


explosion_url = "resources/images/explosion.png"
explosion_details = {"width": 64,"height": 64,"columns": 36,"count": 36,"speed": 0.05,"scale": 3,"looping": False}

bomb_url = "resources/images/granade.png"
bomb_details = {"width": 13,"height": 16,"columns":1,"count": 1,"speed": 0.05,"scale": 2,"looping": False}

class Bomb(Collectable):
    def __init__(self, physics_engine, stats):
        super().__init__(physics_engine, stats, bomb_url, bomb_details)
        self.timeout = 69

    def on_setup(self):
        self.physics_engine.add_sprite(
            self,
            mass=0.1,
            damping=0.01,
            friction=0.3,
            body_type=PymunkPhysicsEngine.DYNAMIC,
            collision_type="placed_bomb",
            elasticity=0.9
        )

    def update(self, delta_time: float = 1/60, *args, **kwargs):
        super().update()
        self.timeout-=1





