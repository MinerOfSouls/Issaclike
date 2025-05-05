from collectables.coin import Coin
from collectables.health_potion import HealthPotion
from collectables.key import Key
from collectables.chest import Chest

#todo use resource handler
key_sprite = 'resources/images/key-white.png'
key_sprite_details = [32,32,12,12,0.3,0.75]

#todo use resource handler
coin_sprite = 'resources/images/coin.png'
coin_sprite_details = [80,80,8,8,0.3,0.25]

#todo use resource handler
chest_sprite = 'resources/images/chest-ss.png'
chest_sprite_details = [48,32,4,4,0.3,2]

#todo use resource handler
health_potion_sprite = 'resources/images/health_potion.png'
health_potion_sprite_details = [16,18,3,3,0.3,1]


class PickupFactory:
    #used to spawn pickups
    # todo add bombs
    def __init__(self , physics_engine, pickups_list, stats):
        self.pickups_list = pickups_list
        self.physics_engine = physics_engine
        self.stats = stats

    def spawn_coin(self,x:int,y:int) -> Coin:
        coin = Coin(self.physics_engine, self.stats,coin_sprite,coin_sprite_details)
        coin.position = x ,y
        self.pickups_list.append(coin)
        coin.on_setup()
        return coin

    def spawn_key(self,x:int,y:int) -> Key:
        key = Key(self.physics_engine, self.stats, key_sprite, key_sprite_details)
        key.position = x ,y
        self.pickups_list.append(key)
        key.on_setup()
        return key

    def spawn_bomb(self,x:int,y:int) -> None:
        pass

    def spawn_chest(self,x:int,y:int):
        chest = Chest(self.physics_engine,self, self.stats,chest_sprite,chest_sprite_details)
        chest.position = x ,y
        self.pickups_list.append(chest)
        chest.on_setup()
        return chest

    def spawn_health_potion(self,x:int,y:int) -> HealthPotion:
        health_potion = HealthPotion(self.physics_engine, self.stats,health_potion_sprite,health_potion_sprite_details)
        health_potion.position  = x,y
        self.pickups_list.append(health_potion)
        health_potion.on_setup()
        return health_potion

    def on_draw(self) -> None:
        self.pickups_list.draw()

    def update(self) -> None:
        self.pickups_list.update()

