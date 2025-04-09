import arcade
class PlayerController:
    def __init__(self, player_sprite,stats):
        self.stats = stats
        self.player = player_sprite
        self.a_pressed = False
        self.d_pressed = False
        self.w_pressed = False
        self.s_pressed = False


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

        # Apply input-based acceleration
        if self.w_pressed and not self.s_pressed:
            self.player.change_y += self.stats.get_acceleration()
        elif self.s_pressed and not self.w_pressed:
            self.player.change_y -= self.stats.get_acceleration()

        if self.a_pressed and not self.d_pressed:
            self.player.change_x -= self.stats.get_acceleration()
        elif self.d_pressed and not self.a_pressed:
            self.player.change_x += self.stats.get_acceleration()

        self.player.change_x = max(-self.stats.get_max_speed(), min(self.stats.get_max_speed(), self.player.change_x))
        self.player.change_y = max(-self.stats.get_max_speed(), min(self.stats.get_max_speed(), self.player.change_y))

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