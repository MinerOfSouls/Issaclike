from parameters import *
from collectables.place_on_map import PlaceOnMap
from random import randint
from collectables.wind_effect import Wind
class DifficultyOptions:
    def __init__(self,game_view):
        self.game_view = game_view
        self.bomb_timeout = 0
        self.change_weapon_timout = 0
        self.place_on_map = self.game_view.place_on_map
        self.physics_engine = self.game_view.physics_engine
        self.player_sprite = self.game_view.player_sprite
        self.wind = Wind(self.physics_engine ,self.game_view.stats)


    def on_setup(self):
        pass

    def spawn_bombs_on_random_position(self):
        width =  randint(int(WINDOW_WIDTH*0.1),int(WINDOW_WIDTH*0.9))
        height = randint(int(WINDOW_HEIGHT*0.1),int(WINDOW_HEIGHT*0.9))
        self.place_on_map.place_bomb(width, height)

    def set_slippery(self):
        body = self.physics_engine.get_physics_object(self.player_sprite).body
        body.damping = 0.9
        # Update friction
        physics_obj = self.physics_engine.get_physics_object(self.player_sprite)
        physics_obj.shape.friction = 0.3

    def modify_attack(self):
        self.game_view.attack_manager.set_random_attack()

    def draw(self):
        self.wind.draw()


    def update(self, delta_time: float = 1 / 60):
        self.wind.update()
        self.bomb_timeout+=1
        self.change_weapon_timout+=1

        if self.bomb_timeout >=60:
            self.spawn_bombs_on_random_position()
            self.bomb_timeout =0
        # if self.change_weapon_timout >= 300:
        #     self.modify_attack()
        #     self.change_weapon_timout =0