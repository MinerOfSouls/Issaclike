import arcade
from parameters import *
# does not follow scaling rules
class Hearth(arcade.Sprite):
    def __init__(self, texture_list: list[arcade.Texture]):
        super().__init__(texture_list[0],scale=1.5)
        self.time_elapsed = 0
        self.textures = texture_list

    def update(self, delta_time: float= 1/60, *args, **kwargs ):
        self.time_elapsed += delta_time
        if self.time_elapsed > 0.3:
            if self.cur_texture_index < len(self.textures):
                self.set_texture(self.cur_texture_index)
                self.cur_texture_index += 1
            self.time_elapsed = 0
        if self.cur_texture_index ==4:
            self.cur_texture_index = 0
