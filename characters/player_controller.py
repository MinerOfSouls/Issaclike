import arcade
import math
class PlayerController:
    def __init__(self, player_sprite,stats):
        self.stats = stats
        self.player = player_sprite
        self.a_pressed = False
        self.d_pressed = False
        self.w_pressed = False
        self.s_pressed = False


    def update(self):
        # Apply self.stats.friction
        if self.player.change_x > self.stats.friction:
            self.player.change_x -= self.stats.friction
        elif self.player.change_x < -self.stats.friction:
            self.player.change_x += self.stats.friction
        else:
            self.player.change_x = 0

        if self.player.change_y > self.stats.friction:
            self.player.change_y -= self.stats.friction
        elif self.player.change_y < -self.stats.friction:
            self.player.change_y += self.stats.friction
        else:
            self.player.change_y = 0

        dx = 0
        dy = 0
        if self.w_pressed and not self.s_pressed:
            dy = 1
        elif self.s_pressed and not self.w_pressed:
            dy = -1
        if self.a_pressed and not self.d_pressed:
            dx = -1
        elif self.d_pressed and not self.a_pressed:
            dx = 1

        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            # Calculate normalization factor (1/sqrt(2))
            norm_factor = 1 / math.sqrt(2)
            dx *= norm_factor
            dy *= norm_factor

        self.player.change_x += dx * self.stats.acceleration
        self.player.change_y += dy * self.stats.acceleration

        current_speed = math.sqrt(self.player.change_x ** 2 + self.player.change_y ** 2)
        max_speed = self.stats.max_speed

        if current_speed > max_speed:
            scale_factor = max_speed / current_speed
            self.player.change_x *= scale_factor
            self.player.change_y *= scale_factor
    def on_key_press(self, key):
        if key == arcade.key.W:
            self.w_pressed = True
        elif key == arcade.key.S:
            self.s_pressed = True
        elif key == arcade.key.A:
            self.a_pressed = True
        elif key == arcade.key.D:
            self.d_pressed = True

    def on_key_release(self, key):
        if key == arcade.key.W:
            self.w_pressed = False
        elif key == arcade.key.S:
            self.s_pressed = False
        elif key == arcade.key.A:
            self.a_pressed = False
        elif key == arcade.key.D:
            self.d_pressed = False