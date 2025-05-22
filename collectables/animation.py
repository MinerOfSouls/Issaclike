import arcade
from physics_util import update_sprite
#rewrite to use texture animation or use only one row sprites

class Animation(arcade.Sprite):
    def __init__(self,texture_list,sprite_details):
        self.animation_speed = sprite_details.get("speed")
        super().__init__(texture_list[0],scale=sprite_details.get("scale"))
        self.time_elapsed = 0
        self.cur_texture_index =0
        self.textures = texture_list
        self.looping = sprite_details.get("looping")
        self.animated = sprite_details.get("animated", True)
        self.should_delete = False

    def update(self, delta_time: float = 1/60, *args, **kwargs):
        if self.animated:
            self.time_elapsed += delta_time
            if self.time_elapsed > self.animation_speed:
                self.time_elapsed = 0
                self.cur_texture_index += 1
                if self.cur_texture_index >= len(self.textures):
                    if self.looping:
                        self.cur_texture_index = 0
                    else:
                        self.cur_texture_index = len(self.textures) - 1
                        self.should_delete = True

            self.set_texture(self.cur_texture_index)