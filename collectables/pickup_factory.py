from pyglet import sprite

from collectables.animation import Animation
from collectables.bomb import Bomb
from collectables.interactive_item import InteractiveItem


from collectables.chest import Chest
from resource_manager import get_object

class PickupFactory:
    def __init__(self , physics_engine, pickups_list, stats):
        self.pickups_list = pickups_list
        self.physics_engine = physics_engine
        self.stats = stats

    def spawn_coin(self,x:int,y:int):
        sprite = get_object("coin")
        coin = InteractiveItem(self.physics_engine, self.stats, sprite[0], sprite[1])
        coin.position = x ,y
        self.pickups_list.append(coin)
        coin.on_setup()
        return coin

    def spawn_key(self,x:int,y:int):
        sprite = get_object("key")
        key = InteractiveItem(self.physics_engine, self.stats, sprite[0], sprite[1])
        key.position = x ,y
        self.pickups_list.append(key)
        key.on_setup()
        return key

    def spawn_bomb(self,x:int,y:int):
        sprite = get_object("bomb")
        bomb = InteractiveItem(self.physics_engine, self.stats, sprite[0], sprite[1])
        bomb.position = x, y
        self.pickups_list.append(bomb)
        bomb.on_setup()
        return bomb

    def spawn_chest(self,x:int,y:int):
        sprite = get_object("chest")
        chest = Chest(self.physics_engine,self, self.stats,sprite[0],sprite[1])
        chest.position = x ,y
        self.pickups_list.append(chest)
        chest.on_setup()
        return chest

    def spawn_health_potion(self,x:int,y:int):
        sprite = get_object("health_potion")
        health_potion = InteractiveItem(self.physics_engine, self.stats, sprite[0], sprite[1])
        health_potion.position  = x,y
        self.pickups_list.append(health_potion)
        health_potion.on_setup()
        return health_potion



