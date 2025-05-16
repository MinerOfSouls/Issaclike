import arcade

from collectables.interactive_item import InteractiveItem
from parameters import *
from random import randint, choice

from resource_manager import get_object


class Wind:
    def __init__(self,physics_engine,stats, map):
        self.physics_engine = physics_engine
        self.stats = stats
        self.effects_list = arcade.SpriteList()
        self.map = map
        self.direction = None
        self.cooldown = 0

    def on_setup(self):
        pass

    def change_gravity(self, direction):
        gravity_map = {
            "up": (0, 250),
            "left": (-250, 0),
            "right": (250, 0),
            "down": (0, -250)
        }
        self.physics_engine.space.gravity = gravity_map.get(direction, (0, 0))

    def spawn_leaf(self, x: int, y: int):
        sprite = get_object("leaf")
        leaf = InteractiveItem(self.physics_engine, self.stats,
                               sprite[0], sprite[1])
        leaf.position = (x, y)
        leaf.on_setup()
        self.effects_list.append(leaf)

    def spawn_leafs(self, wind_direction):

        edge_spawns = {
            "up": lambda: (randint(0, WINDOW_WIDTH), randint(-50, -2)),
            "left": lambda: (randint(WINDOW_WIDTH+2, WINDOW_WIDTH + 50), randint(0, WINDOW_HEIGHT)),
            "right": lambda: (randint(-50, -2), randint(0, WINDOW_HEIGHT)),
            "down": lambda: (randint(0, WINDOW_WIDTH), randint(WINDOW_HEIGHT+2, WINDOW_HEIGHT + 50))
        }
        spawn_func = edge_spawns.get(wind_direction, lambda: (0, 0))
        for _ in range(WINDOW_WIDTH // 512):
            if randint(0, 1):
                self.spawn_leaf(*spawn_func())

    def remove_off_screen(self):
        for leaf in self.effects_list:
            if (leaf.center_x > WINDOW_WIDTH or leaf.center_y>WINDOW_HEIGHT or leaf.center_x <0 or leaf.center_y <0) and leaf.item_lifetime >120:
                self.effects_list.remove(leaf)

    def draw(self):
        self.effects_list.draw()

    # must be before loading room elements
    def update(self):
        self.cooldown+=1
        self.effects_list.update()
        self.remove_off_screen()
        if not self.map.is_loaded():
            self.direction = choice(["left","right","up","down"])
            self.change_gravity(self.direction)
        if self.cooldown>20:
            self.spawn_leafs(self.direction)
            self.cooldown =0



