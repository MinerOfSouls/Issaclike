from characters.sword import  Sword
import math
class SwordCreator:
    def __init__(self,physics_engine,player_sprite,sword_list,stats):
        self.physics_engine = physics_engine
        self.stats = stats
        self.player_sprite = player_sprite
        self.sword_list = sword_list


    def spawn_sword(self):
        sword = Sword(self.physics_engine,self.stats)
        self.sword_list.append(sword)
        sword.on_setup()
        return sword