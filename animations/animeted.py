import arcade
import math

def facing_to_direction(angle):
    if angle < 30 or angle >= 330:
        return "north"
    elif 30 <= angle < 150:
        return "east"
    elif 150 <= angle < 210:
        return "south"
    elif 210 <= angle < 330:
        return "west"

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
        self.texture_update_distance = 20
        self.last_update = (self.center_x, self.center_y)
        self.facing_calc = facing_to_direction

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        dx = self.last_update[0] - self.center_x
        dy = self.last_update[1] - self.center_y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist == 0:
            self.texture = self.standing_animations[self.facing_calc(self.facing)][self.current_standing_texture_index]
            self.current_standing_texture_index = (self.current_standing_texture_index + 1)%self.standing_animation_length
        if dist < self.texture_update_distance:
            return
        self.facing = math.degrees(math.atan2(dx, dy) - math.pi/2)%360
        self.texture = self.moving_animations[self.facing_calc(self.facing)][self.current_texture_index]
        self.current_texture_index = (self.current_texture_index + 1)%self.moving_animation_length
        self.last_update = (self.center_x, self.center_y)
