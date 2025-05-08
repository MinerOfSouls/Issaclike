import arcade

from collectables.collectable import Collectable
from parameters import *
from random import randint


wind_particle_url = "resources/images/ELR_FallLeaf.png"
wind_particle_details = {
    "width": 16,
    "height": 16,
    "columns": 5,
    "count": 5,
    "speed": 0.3,
    "scale": 2,
    "looping": True,
    "collectable": False,
    "item_type": "leaf"
}

class Wind:
    def __init__(self,physics_engine,stats):
        self.physics_engine = physics_engine
        self.stats = stats
        self.effects_list = arcade.SpriteList()
        self.cooldown = 300


    def change_gravity(self, direction):
        """Change gravity direction and magnitude (500 units)"""
        gravity_map = {
            "up": (0, 500),
            "left": (-500, 0),
            "right": (500, 0),
            "down": (0, -500)
        }
        self.physics_engine.space.gravity = gravity_map.get(direction, (0, 0))

    def spawn_leaf(self, x: int, y: int):
        """Create a leaf collectable at specified position"""
        leaf = Collectable(self.physics_engine, self.stats,
                           wind_particle_url, wind_particle_details)
        leaf.position = (x, y)
        leaf.on_setup()
        self.effects_list.append(leaf)

    def directional_wind(self, wind_direction):
        """Spawn leaves along the edge opposite to wind direction"""
        self.change_gravity(wind_direction)

        edge_spawns = {
            "up": lambda: (randint(0, WINDOW_WIDTH), randint(-50, -2)),
            "left": lambda: (randint(WINDOW_WIDTH+2, WINDOW_WIDTH + 50), randint(0, WINDOW_HEIGHT)),
            "right": lambda: (randint(-50, -2), randint(0, WINDOW_HEIGHT)),
            "down": lambda: (randint(0, WINDOW_WIDTH), randint(WINDOW_HEIGHT+2, WINDOW_HEIGHT + 50))
        }
        # Spawn leaves along the appropriate edge
        spawn_func = edge_spawns.get(wind_direction, lambda: (0, 0))
        for _ in range(WINDOW_WIDTH // 64):  # Fixed number of leaves
            if randint(0, 1):  # 50% chance to spawn at each position
                self.spawn_leaf(*spawn_func())

    def draw(self):
        self.effects_list.draw()

    def remove_off_screen(self):
        for leaf in self.effects_list:
            if (leaf.center_x > WINDOW_WIDTH or leaf.center_y>WINDOW_HEIGHT or leaf.center_x <0 or leaf.center_y <0) and leaf.item_lifetime >120:
                self.effects_list.remove(leaf)

    def update(self):
        self.effects_list.update()
        self.cooldown+=1
        self.remove_off_screen()
        if self.cooldown >45:
            self.directional_wind("up")
            self.cooldown = 0




