from collectables.coin import Coin
from collectables.key import Key
from collectables.chest import Chest


class PickupFactory:
    #used to spawn pickups
    # todo add bombs
    def __init__(self , physics_engine, pickups_list, stats):
        self.pickups_list = pickups_list
        self.physics_engine = physics_engine
        self.stats = stats

    def spawn_coin(self,x:int,y:int) -> Coin:
        coin = Coin(self.physics_engine, self.stats)
        coin.position = x ,y
        self.pickups_list.append(coin)
        coin.on_setup()
        return coin

    def spawn_key(self,x:int,y:int) -> Key:
        key = Key(self.physics_engine, self.stats)
        key.position = x ,y
        self.pickups_list.append(key)
        key.on_setup()
        return key

    def spawn_bomb(self,x:int,y:int) -> None:
        pass

    def spawn_chest(self,x:int,y:int):
        chest = Chest(self.physics_engine,self, self.stats)
        chest.position = x ,y
        self.pickups_list.append(chest)
        chest.on_setup()
        return chest

    def on_draw(self) -> None:
        self.pickups_list.draw()
        # self.bomb_list.draw()

    def update(self) -> None:
        self.pickups_list.update()

