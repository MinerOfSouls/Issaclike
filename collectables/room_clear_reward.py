import random

from collectables.chest import Chest
from collectables.pickup_factory import PickupType, PickupFactory
from effects.item_effects import ItemEffects
from parameters import *
from resource_manager import get_object


class SpawnRandomReward:
    def __init__(self, physics_engine, item_list ,effect_list, stats):
        self.physics_engine = physics_engine
        self.item_list = item_list
        self.effect_list = effect_list
        self.stats = stats
        self.pickup_factory = PickupFactory(self.physics_engine, self.item_list, self.stats)


    def _spawn_chest(self):
        ItemEffects.item_spawn_effect(self.physics_engine, self.stats, self.effect_list,(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 0.2)
        sprite = get_object("chest")
        chest = Chest(self.physics_engine, self.pickup_factory, self.stats, sprite[0], sprite[1])
        chest.position = WINDOW_WIDTH/2 , WINDOW_HEIGHT/2
        chest.on_setup()
        self.item_list.append(chest)
        return chest

    def _spawn_random_collectable(self):
        random_pickup = random.choice(list(PickupType))
        ItemEffects.item_spawn_effect(self.physics_engine, self.stats , self.effect_list , (WINDOW_WIDTH/2,WINDOW_HEIGHT/2),0.1)
        return self.pickup_factory.create_pickup(random_pickup, WINDOW_WIDTH/2 , WINDOW_HEIGHT/2)

    def on_room_clear(self):
        random_chance = random.randint(0,10) + self.stats.luck
        print(random_chance, end=" ")
        if random_chance < 2:
            print("nothing")
        elif random_chance < 9:
            item = self._spawn_random_collectable()
            print(item)
            return item
        else:
            item =  self._spawn_chest()
            print(item)
            return item
