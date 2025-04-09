import arcade

from parameters import *
class Player(arcade.Sprite):

    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
            self.change_x = 0
        elif self.right > WINDOW_WIDTH - 1:
            self.right = WINDOW_WIDTH - 1
            self.change_x = 0
        if self.bottom < 0:
            self.bottom = 0
            self.change_y = 0
        elif self.top > WINDOW_HEIGHT - 1:
            self.top = WINDOW_HEIGHT - 1
            self.change_y = 0