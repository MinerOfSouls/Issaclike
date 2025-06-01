from random import randint

from collectables.base.interactive_item import InteractiveItem
from effects.item_effects import ItemEffects
from resource_manager import get_object
from parameters import *


class RandomExplosions:
    def __init__(self, physics_engine, effects_list, stats):
        self.physics_engine = physics_engine
        self.stats = stats
        self.effects_list = effects_list
        self.indicators = arcade.SpriteList()
        self.bomb_timeout = 0

    def on_setup(self):
        pass

    def spawn_explosions_on_random_position(self):
        width = randint(int(WINDOW_WIDTH * 0.1), int(WINDOW_WIDTH * 0.9))
        height = randint(int(WINDOW_HEIGHT * 0.1), int(WINDOW_HEIGHT * 0.9))
        sprite = get_object("skull")
        skull = InteractiveItem(self.physics_engine, self.stats, sprite[0], sprite[1])
        skull.position = (width, height)
        skull.on_setup()
        self.indicators.append(skull)

    def draw(self):
        self.indicators.draw()
        self.effects_list.draw()

    def update(self):
        self.indicators.update()
        self.effects_list.update()
        self.bomb_timeout += 1

        for indicator in self.indicators:
            if indicator.item_lifetime >= 70:
                ItemEffects.explode(self.physics_engine, self.stats, self.effects_list, indicator.position)
                self.indicators.remove(indicator)
                self.physics_engine.remove_sprite(indicator)
        for effect in self.effects_list:
            if effect.should_delete:
                self.effects_list.remove(effect)
                self.physics_engine.remove_sprite(effect)

        if self.bomb_timeout >= 60:
            self.spawn_explosions_on_random_position()
            self.bomb_timeout = 0
