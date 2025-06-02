import arcade
from arcade import PymunkPhysicsEngine

from characters.stats import Stats
from collectables.base.interactive_item import InteractiveItem
from effects.item_effects import ItemEffects
from resource_manager import get_object


class Bomb(InteractiveItem):
    def __init__(self, physics_engine: PymunkPhysicsEngine, stats: Stats, effect_list: arcade.SpriteList,
                 placed_items: arcade.SpriteList):
        super().__init__(physics_engine, stats, get_object("placed_bomb")[0], get_object("placed_bomb")[1])
        self.physics_engine = physics_engine
        self.effect_list = effect_list
        self.placed_items = placed_items
        self.original_color = (255, 255, 255)
        self.color = self.original_color

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        super().update()
        self.item_lifetime += 1
        red_intensity = (self.item_lifetime / 70.0)

        red = 255
        green = int(self.original_color[1] * (1 - red_intensity))
        blue = int(self.original_color[2] * (1 - red_intensity))

        self.color = (red, green, blue)

        if self.item_lifetime >= 70:
            self.physics_engine.remove_sprite(self)
            self.placed_items.remove(self)
            ItemEffects.explode(self.physics_engine, self.stats, self.effect_list, self.position)
