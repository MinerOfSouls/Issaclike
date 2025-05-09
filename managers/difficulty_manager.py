import arcade
from arcade import PymunkPhysicsEngine

from collectables.interactive_item import InteractiveItem
from effects.item_effects import ItemEffects
from parameters import *
from random import randint
from effects.wind_effect import Wind
squll_url = 'resources/images/Skull 004 16x161.png'
squll_sprite_details = {
    "width": 16,
    "height": 16,
    "columns": 1,
    "count": 1,
    "speed": 0.3,
    "scale": 2,
    "looping": False,
    "collectable": False,
    "item_type": "spawn_indicator",
    "body_type": PymunkPhysicsEngine.KINEMATIC
}
class DifficultyOptions:
    def __init__(self,physics_engine ,player_sprite, stats ,effects_list):
        self.physics_engine = physics_engine
        self.player_sprite = player_sprite
        self.stats = stats
        self.effects_list = effects_list
        self.indicators = arcade.SpriteList()
        self.bomb_timeout = 0
        self.change_weapon_timout = 0
        self.wind = Wind(self.physics_engine ,self.stats)


    def on_setup(self):
        pass

    def spawn_explosions_on_random_position(self):
        width =  randint(int(WINDOW_WIDTH*0.1),int(WINDOW_WIDTH*0.9))
        height = randint(int(WINDOW_HEIGHT*0.1),int(WINDOW_HEIGHT*0.9))
        skull = InteractiveItem(self.physics_engine,self.stats, squll_url ,squll_sprite_details)
        skull.position = (width,height)
        skull.on_setup()
        self.indicators.append(skull)

    def modify_attack(self):
        # self.attack_manager.set_random_attack()
        pass

    def draw(self):
        self.wind.draw()
        self.indicators.draw()
        self.effects_list.draw()


    def update(self, delta_time: float = 1 / 60):
        self.wind.update()
        self.indicators.update()
        self.effects_list.update()
        self.bomb_timeout+=1
        self.change_weapon_timout+=1

        for indicator in self.indicators:
            if indicator.item_lifetime >=70:
                ItemEffects.explode(self.physics_engine, self.stats, self.effects_list, indicator.position)
                self.indicators.remove(indicator)
                self.physics_engine.remove_sprite(indicator)
        for effect in self.effects_list:
            if effect.should_delete:
                self.effects_list.remove(effect)
                self.physics_engine.remove_sprite(effect)

        if self.bomb_timeout >=60:
            self.spawn_explosions_on_random_position()
            self.bomb_timeout =0
        if self.change_weapon_timout >= 300:
            self.modify_attack()
            self.change_weapon_timout =0