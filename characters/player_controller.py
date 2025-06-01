import arcade
import math

from characters.stats import Stats


class PlayerController:
    def __init__(self, player_sprite :arcade.Sprite, stats :Stats):
        self.stats = stats
        self.player = player_sprite
        self.a_pressed = False
        self.d_pressed = False
        self.w_pressed = False
        self.s_pressed = False

        self.diagonal_up_right = False
        self.diagonal_up_left = False
        self.diagonal_down_right = False
        self.diagonal_down_left = False

        self.direction = 0

        self.player.properties["invincible"] = False
        self.player.properties["inv_timer"] = 0

    def on_update(self,physics_engine) -> None:

        dx = 0
        dy = 0
        if self.w_pressed and not self.s_pressed:
                dy = 200
        elif self.s_pressed and not self.w_pressed:
                dy = -200
        if self.a_pressed and not self.d_pressed:
                dx = -200
        elif self.d_pressed and not self.a_pressed:
                dx = 200

        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            norm_factor = 1 / math.sqrt(2)
            dx *= norm_factor
            dy *= norm_factor

        speed = self.stats.speed
        velocity = (dx * speed, dy * speed)
        physics_engine.apply_force(self.player,velocity)

    def on_key_press(self, key):
        if key == arcade.key.W:
            self.w_pressed = True
        elif key == arcade.key.S:
            self.s_pressed = True
        elif key == arcade.key.A:
            self.a_pressed = True
        elif key == arcade.key.D:
            self.d_pressed = True

        self.update_direction()

    def on_key_release(self, key):
        if key == arcade.key.W:
            self.w_pressed = False
        elif key == arcade.key.S:
            self.s_pressed = False
        elif key == arcade.key.A:
            self.a_pressed = False
        elif key == arcade.key.D:
            self.d_pressed = False

        self.update_direction()

    def update_direction(self):
        self.diagonal_up_right = self.w_pressed and self.d_pressed
        self.diagonal_up_left = self.w_pressed and self.a_pressed
        self.diagonal_down_right = self.s_pressed and self.d_pressed
        self.diagonal_down_left = self.s_pressed and self.a_pressed

        # Calculate direction based on key combinations
        if self.diagonal_up_right:
            self.direction = 45  # Northeast
        elif self.diagonal_up_left:
            self.direction = 135  # Northwest
        elif self.diagonal_down_left:
            self.direction = 225  # Southwest
        elif self.diagonal_down_right:
            self.direction = 315  # Southeast
        elif self.d_pressed:
            self.direction = 0  # East
        elif self.w_pressed:
            self.direction = 90  # North
        elif self.a_pressed:
            self.direction = 180  # West
        elif self.s_pressed:
            self.direction = 270  # South