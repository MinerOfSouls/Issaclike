import arcade
import math
class PlayerController:
    def __init__(self, player_sprite, stats):
        self.stats = stats
        self.player = player_sprite
        self.a_pressed = False
        self.d_pressed = False
        self.w_pressed = False
        self.s_pressed = False

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
            # Calculate normalization factor (1/sqrt(2))
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

    def on_key_release(self, key):
        if key == arcade.key.W:
            self.w_pressed = False
        elif key == arcade.key.S:
            self.s_pressed = False
        elif key == arcade.key.A:
            self.a_pressed = False
        elif key == arcade.key.D:
            self.d_pressed = False