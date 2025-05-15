import math

import arcade
from arcade import PymunkPhysicsEngine


from collectables.interactive_item import InteractiveItem
from effects.item_effects import ItemEffects
from parameters import *
from random import randint
from effects.wind_effect import Wind
from resource_manager import get_object


class DifficultyOptions:
    def __init__(self,physics_engine ,player_sprite, stats ,effects_list,attack_manager):
        self.physics_engine = physics_engine
        self.player_sprite = player_sprite
        self.stats = stats
        self.attack_manager = attack_manager
        self.effects_list = effects_list
        self.indicators = arcade.SpriteList()
        self.bomb_timeout = 0
        self.change_weapon_timout = 0
        self.fire_timeout = 0
        self.moving_fire =None
        self.wind = Wind(self.physics_engine ,self.stats)


    def spawn_explosions_on_random_position(self):
        width =  randint(int(WINDOW_WIDTH*0.1),int(WINDOW_WIDTH*0.9))
        height = randint(int(WINDOW_HEIGHT*0.1),int(WINDOW_HEIGHT*0.9))
        sprite = get_object("skull")
        skull = InteractiveItem(self.physics_engine,self.stats, sprite[0] ,sprite[1])
        skull.position = (width,height)
        skull.on_setup()
        self.indicators.append(skull)

    def modify_attack(self):
        self.attack_manager.set_random_attack()
        pass

    def __move_calc(self,object, destination):
        x_goal = destination[0]
        y_goal = destination[1]
        x_delta = x_goal - object.center_x
        y_delta = y_goal - object.center_y
        angle = math.atan2(y_delta, x_delta)
        dist = math.dist(object.position, destination)
        speed = min(1.0, dist)
        change_x = math.cos(angle) * speed
        change_y = math.sin(angle) * speed
        return change_x, change_y

    def basic_move(self,sprite, destination):
        change_x, change_y = self.__move_calc(sprite,destination)
        self.physics_engine.apply_impulse(sprite, (change_x, change_y))


    def spawn_more_fire(self):
        x = self.player_sprite.center_x +50
        y = self.player_sprite.center_y
        static_fire = get_object("static_fire")
        static_fire = InteractiveItem(self.physics_engine,self.stats, static_fire[0], static_fire[1])
        static_fire.position = self.moving_fire.position
        static_fire.on_setup()
        self.effects_list.append(static_fire)

    def on_setup(self):
        x = self.player_sprite.center_x +50
        y = self.player_sprite.center_y
        fire_sprite = get_object("wisp")
        self.moving_fire = InteractiveItem(self.physics_engine,self.stats, fire_sprite[0], fire_sprite[1])
        self.moving_fire.position = (x,y)
        self.moving_fire.on_setup()
        self.effects_list.append(self.moving_fire)


    def draw(self):
        self.wind.draw()
        self.indicators.draw()
        self.effects_list.draw()

    def update(self, delta_time: float = 1 / 60):
        # self.wind.update()
        self.indicators.update()
        self.effects_list.update()
        self.bomb_timeout+=1
        self.fire_timeout+=1
        self.change_weapon_timout+=1

        if self.fire_timeout >10:
            self.spawn_more_fire()
            self.fire_timeout = 0

        for effect in self.effects_list:
            if effect.item_type == "wisp":
                self.basic_move(effect, self.player_sprite.position)
            if effect.item_type == "static_fire" and effect.item_lifetime >90:
                self.physics_engine.remove_sprite(effect)
                self.effects_list.remove(effect)

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
        # if self.change_weapon_timout >= 300:
        #     self.modify_attack()
        #     self.change_weapon_timout =0