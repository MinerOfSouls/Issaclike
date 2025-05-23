import arcade
import math
from physics_util import update_sprite


def facing_to_direction(angle):
    if angle < 60 or angle >= 300:
        return "east"
    elif 60 <= angle < 120:
        return "north"
    elif 120 <= angle < 240:
        return "west"
    elif 240 <= angle < 300:
        return "south"

class AnimatedMovingSprite(arcade.Sprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.facing = 0
        self.standing_animations = {"west":[], "east":[], "north":[], "south":[]}
        self.moving_animations = {"west":[], "east":[], "north":[], "south":[]}
        self.current_texture_index = 0
        self.current_standing_texture_index = 0
        self.standing_animation_length = 0 #have to set
        self.moving_animation_length = 0
        self.texture_update_distance = 5
        self.last_update = (self.center_x, self.center_y)
        self.facing_calc = facing_to_direction
        self.standing_time = 0

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        dx = self.last_update[0] - self.center_x
        dy = self.last_update[1] - self.center_y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist == 0:
            self.standing_time += 1
            if self.standing_time > 5:
                self.texture = self.standing_animations[self.facing_calc(self.facing)][
                    self.current_standing_texture_index]
                self.current_standing_texture_index = (self.current_standing_texture_index + 1) % self.standing_animation_length
        self.standing_time = 0
        if dist < self.texture_update_distance:
            return
        self.facing = math.degrees(math.atan2(dx, dy) - math.pi/2)%360
        self.texture = self.moving_animations[self.facing_calc(self.facing)][self.current_texture_index]
        self.sync_hit_box_to_texture()
        self.current_texture_index = (self.current_texture_index + 1)%self.moving_animation_length
        self.last_update = (self.center_x, self.center_y)
        for engine in self.physics_engines:
            update_sprite(engine, self)
