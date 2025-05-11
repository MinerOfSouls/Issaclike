from collectables.animation import Animation
from collectables.interactive_item import InteractiveItem


from collectables.chest import Chest

# todo use resource handler
key_sprite = 'resources/images/key-white.png'
key_sprite_details = {
    "width": 32,
    "height": 32,
    "columns": 12,
    "count": 12,
    "speed": 0.3,
    "scale": 0.75,
    "looping": True,
    "collectable": True,
    "item_type": "pick_key",
}

# todo use resource handler
coin_sprite = 'resources/images/coin.png'
coin_sprite_details = {
    "width": 80,
    "height": 80,
    "columns": 8,
    "count": 8,
    "speed": 0.3,
    "scale": 0.25,
    "looping": True,
    "collectable": True,
    "item_type": "pick_coin",
}

# todo use resource handler
chest_sprite = 'resources/images/chest-ss.png'
chest_sprite_details = {
    "width": 48,
    "height": 32,
    "columns": 4,
    "count": 4,
    "speed": 0.3,
    "scale": 2,
    "looping": False
}

# todo use resource handler
health_potion_sprite = 'resources/images/health_potion.png'
health_potion_details = {
    "width": 16,
    "height": 18,
    "columns": 3,
    "count": 3,
    "speed": 0.3,
    "scale": 1,
    "looping": True,
    "collectable": True,
    "item_type": "pick_health_potion",
}

bomb_url = "resources/images/granade.png"
bomb_details = {
    "width": 13,
    "height": 16,
    "columns":1,
    "count": 1,
    "speed": 0.05,
    "scale": 2,
    "looping": False,
    "collectable": True,
    "item_type": "pick_bomb"
}

# todo wait for resource handler now it looks like this and it is bad

class PickupFactory:
    def __init__(self , physics_engine, pickups_list, stats):
        self.pickups_list = pickups_list
        self.physics_engine = physics_engine
        self.stats = stats

    def spawn_coin(self,x:int,y:int):
        coin = InteractiveItem(self.physics_engine, self.stats, coin_sprite, coin_sprite_details)
        coin.position = x ,y
        self.pickups_list.append(coin)
        coin.on_setup()
        return coin

    def spawn_key(self,x:int,y:int):
        key = InteractiveItem(self.physics_engine, self.stats, key_sprite, key_sprite_details)
        key.position = x ,y
        self.pickups_list.append(key)
        key.on_setup()
        return key

    def spawn_bomb(self,x:int,y:int):
        bomb = InteractiveItem(self.physics_engine, self.stats, bomb_url, bomb_details)
        bomb.position = x, y
        self.pickups_list.append(bomb)
        bomb.on_setup()
        return bomb

    def spawn_chest(self,x:int,y:int):
        chest = Chest(self.physics_engine,self, self.stats,chest_sprite,chest_sprite_details)
        chest.position = x ,y
        self.pickups_list.append(chest)
        chest.on_setup()
        return chest

    def spawn_health_potion(self,x:int,y:int):
        health_potion = InteractiveItem(self.physics_engine, self.stats, health_potion_sprite, health_potion_details)
        health_potion.position  = x,y
        self.pickups_list.append(health_potion)
        health_potion.on_setup()
        return health_potion


