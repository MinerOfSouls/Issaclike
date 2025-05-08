from arcade import PymunkPhysicsEngine
from collectables.animation import Animation
from collectables.collectable import Collectable
from pickup_factory import PickupFactory

explosion_url = "resources/images/explosion.png"
explosion_details = {
    "width": 64,
    "height": 64,
    "columns": 30,
    "count": 30,
    "speed": 0.05,
    "scale": 3,
    "looping": False,
    "collectable": False,
    "item_type": "explosion",
    "body_type": PymunkPhysicsEngine.KINEMATIC,
    "mass": 10000
}

bomb_url = "resources/images/granade.png"
bomb_details = {
    "width": 13,
    "height": 16,
    "columns": 1,
    "count": 1,
    "speed": 0.05,
    "scale": 2,
    "looping": False
}


class Bomb(Collectable):
    def __init__(self, physics_engine, stats, effect_list,placed_items):
        super().__init__(physics_engine, stats, bomb_url, bomb_details)
        self.timeout = 69
        self.effect_list = effect_list
        self.placed_items = placed_items
        self.original_color = (255, 255, 255)  # Store original color
        self.color = self.original_color  # Initialize color

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

    def explode(self):
        explosion = Collectable(self.physics_engine, self.stats, explosion_url, explosion_details)
        explosion.position = self.position
        explosion.on_setup()
        self.effect_list.append(explosion)

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        super().update()
        self.timeout -= 1

        # Calculate red intensity based on remaining time (0-1)
        red_intensity = 1.0 - (self.timeout / 69.0)

        # Interpolate between original color and full red
        red = 255  # Full red
        green = int(self.original_color[1] * (1 - red_intensity))
        blue = int(self.original_color[2] * (1 - red_intensity))

        self.color = (red, green, blue)

        if self.timeout <= 0:
            self.explode()
            self.placed_items.remove(self)
            self.physics_engine.remove_sprite(self)