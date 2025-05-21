import arcade
from item import Item
from parameters import *

class Inventory:
    def __init__(self):
        self.items: list[Item] = []
        self.item_sprites = arcade.SpriteList()
        self.i = 0
        self.extra_objects = arcade.SpriteList()

    def update(self, **kwargs):
        for item in self.items:
            item.update(**kwargs)

    def on_key_press(self, key, **kwargs):
        if key == arcade.key.KEY_1 and self.i > 0:
            self.items[0].activated(**kwargs, objects = self.extra_objects)
        elif key == arcade.key.KEY_2 and self.i > 1:
            self.items[1].activated(**kwargs, objects = self.extra_objects)
        elif key == arcade.key.KEY_3 and self.i > 2:
            self.items[2].activated(**kwargs, objects = self.extra_objects)
        elif key == arcade.key.KEY_4 and self.i > 3:
            self.items[3].activated(**kwargs, objects = self.extra_objects)
        elif key == arcade.key.KEY_5 and self.i > 4:
            self.items[4].activated(**kwargs, objects = self.extra_objects)
        elif key == arcade.key.KEY_6 and self.i > 5:
            self.items[5].activated(**kwargs, objects = self.extra_objects)

    def add_item(self, thing: Item):
        self.items.append(thing)
        self.item_sprites.append(thing.sprite)
        thing.sprite.top = WINDOW_HEIGHT
        thing.sprite.left = WINDOW_WIDTH - 150 + 25*self.i
        self.i += 1

    def draw(self):
        self.item_sprites.draw()
        self.extra_objects.draw()