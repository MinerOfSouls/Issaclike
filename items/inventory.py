import arcade
from rooms import BossRoom
from items.item import Item
from items.things import name_to_item, get_new_item
from parameters import *
import json
import os

class Inventory:
    def __init__(self):
        self.items: list[Item] = []
        self.item_sprites = arcade.SpriteList()
        self.i = 0
        self.extra_objects = arcade.SpriteList()

    def update(self, **kwargs):
        for item in self.items:
            item.update(**kwargs, objects = self.extra_objects)
        mapp = kwargs["map"]
        if (mapp.rooms[mapp.current_room].completed and type(mapp.rooms[mapp.current_room]) is BossRoom
            and not mapp.rooms[mapp.current_room].item_given):
            mapp.rooms[mapp.current_room].item_given = True
            new = get_new_item(self.items)
            if new:
                self.add_item(new)

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
        thing.sprite.top = WINDOW_HEIGHT - 165
        thing.sprite.left = WINDOW_WIDTH - 210 + 30*self.i
        self.i += 1

    def draw(self):
        self.item_sprites.draw()
        self.extra_objects.draw()

    def save(self):
        l = [str(i) for i in self.items]
        f = open("inventory.json", "w+")
        json.dump(l, f)
        f.close()

    def load(self):
        if not os.path.isfile("inventory.json"):
            return
        f = open("inventory.json", "r")
        l = json.load(f)
        f.close()
        for name in l:
            self.add_item(name_to_item(name))
        print(self.items)