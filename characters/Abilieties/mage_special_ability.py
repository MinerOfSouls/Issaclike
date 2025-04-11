import arcade

from characters.Abilieties.special_ability import SpecialAbility


class MageSpecialAbility(SpecialAbility):
    TELEPORT_DISTANCE = 50  # Distance to teleport in pixels
    COOLDOWN = 23  # Cooldown in frames (1 second at 60 FPS)

    def __init__(self, player_sprite):
        super().__init__(player_sprite)
        self.teleporting = False
        self.cooldown = 0


    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

        # Reset velocity if teleporting (optional)
        if self.teleporting:
            self.player.change_x = 0
            self.player.change_y = 0
            self.teleporting = False

    def attempt_teleport(self):
        if self.cooldown <= 0 and self.space_pressed:
            self.cooldown = self.COOLDOWN
            self.teleporting = True

            direction_x = 0
            direction_y = 0

            if self.w_pressed and not self.s_pressed:
                direction_y = 1
            elif self.s_pressed and not self.w_pressed:
                direction_y = -1

            if self.a_pressed and not self.d_pressed:
                direction_x = -1
            elif self.d_pressed and not self.a_pressed:
                direction_x = 1

            # If no direction keys are pressed, don't teleport
            if direction_x == 0 and direction_y == 0:
                return

            # Normalize diagonal movement to maintain consistent distance
            if direction_x != 0 and direction_y != 0 :
                length = (direction_x ** 2 + direction_y ** 2) ** 0.5
                direction_x /= length
                direction_y /= length

            self.player.center_x += direction_x * self.TELEPORT_DISTANCE
            self.player.center_y += direction_y * self.TELEPORT_DISTANCE
    def on_key_press(self, key):
        super().on_key_press(key)
        if key == arcade.key.SPACE:
            self.attempt_teleport()