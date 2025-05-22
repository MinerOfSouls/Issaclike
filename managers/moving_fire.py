import arcade
from setuptools.archive_util import unpack_zipfile

from collectables.interactive_item import InteractiveItem
from parameters import *
import math

from resource_manager import get_object


class MovingFire:
    def __init__(self,physics_engine ,player_sprite,effects_list, stats):
        self.physics_engine = physics_engine
        self.player_sprite = player_sprite
        self.stats = stats
        self.effects_list = effects_list
        self.fire_timeout = 0
        self.moving_fire = None

    # zajebałem z enemy
    def __move_calc(self, object, destination):
        x_goal = destination[0]
        y_goal = destination[1]
        x_delta = x_goal - object.center_x
        y_delta = y_goal - object.center_y
        angle = math.atan2(y_delta, x_delta)
        dist = math.dist(object.position, destination)
        speed = min(1.0, dist)
        change_x = math.cos(angle) * speed
        change_y = math.sin(angle) * speed
        return change_x, change_y

    def basic_move(self, sprite, destination):
        change_x, change_y = self.__move_calc(sprite, destination)
        self.physics_engine.apply_impulse(sprite, (change_x, change_y))

    def spawn_more_fire(self):
        static_fire = get_object("static_fire")
        static_fire = InteractiveItem(self.physics_engine,self.stats, static_fire[0], static_fire[1])
        static_fire.position = self.moving_fire.position
        static_fire.on_setup()
        self.effects_list.append(static_fire)

    def on_setup(self):
        x = WINDOW_WIDTH -30
        y = WINDOW_HEIGHT - 30
        fire_sprite = get_object("wisp")
        self.moving_fire = InteractiveItem(self.physics_engine,self.stats, fire_sprite[0], fire_sprite[1])
        self.moving_fire.position = (x,y)
        self.moving_fire.on_setup()
        self.effects_list.append(self.moving_fire)

    def draw(self):
        self.effects_list.draw()

    def update(self):
        self.effects_list.update()
        self.fire_timeout += 1

        if self.fire_timeout >10:
            self.spawn_more_fire()
            self.fire_timeout = 0

        for effect in self.effects_list:
            if effect.item_type == "wisp":
                self.basic_move(effect, self.player_sprite.position)
            if effect.item_type == "static_fire" and effect.item_lifetime >90:
                self.physics_engine.remove_sprite(effect)
                self.effects_list.remove(effect)