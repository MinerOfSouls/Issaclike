import arcade
import math
class PlayerController:
    def __init__(self, player_sprite, stats, engine: arcade.PymunkPhysicsEngine):
        self.stats = stats
        self.player = player_sprite
        self.a_pressed = False
        self.d_pressed = False
        self.w_pressed = False
        self.s_pressed = False

        self.physics_engine = engine



    def update(self):
        # Apply self.stats.get_friction()
        if self.player.change_x > self.stats.get_friction():
            self.player.change_x -= self.stats.get_friction()
        elif self.player.change_x < -self.stats.get_friction():
            self.player.change_x += self.stats.get_friction()
        else:
            self.player.change_x = 0

        if self.player.change_y > self.stats.get_friction():
            self.player.change_y -= self.stats.get_friction()
        elif self.player.change_y < -self.stats.get_friction():
            self.player.change_y += self.stats.get_friction()
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

        change_x = dx * self.stats.get_acceleration()
        change_y = dy * self.stats.get_acceleration()

        self.physics_engine.apply_force(self.player, (1000*change_x, 1000*change_y))

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