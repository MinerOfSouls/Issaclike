import arcade

class Attack:
    def __init__(self, player_sprite, stats):
        self.player = player_sprite
        self.stats = stats

        # Direction keys
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        # Action key
        self.e_pressed = False

        # Keep track of diagonal states
        self.diagonal_up_right = False
        self.diagonal_up_left = False
        self.diagonal_down_right = False
        self.diagonal_down_left = False

        # Current direction angle (in degrees, 0 = right, 90 = up, etc.)
        self.direction = 0

    def on_key_press(self, key):
        if key == arcade.key.UP:
            self.up_pressed = True
        if key == arcade.key.DOWN:
            self.down_pressed = True
        if key == arcade.key.LEFT:
            self.left_pressed = True
        if key == arcade.key.RIGHT:
            self.right_pressed = True
        if key == arcade.key.E:
            self.e_pressed = True

        # Update diagonal states and direction after any key press
        self.update_direction()

    def on_key_release(self, key):
        # Use separate if statements for direction keys
        if key == arcade.key.UP:
            self.up_pressed = False
        if key == arcade.key.DOWN:
            self.down_pressed = False
        if key == arcade.key.LEFT:
            self.left_pressed = False
        if key == arcade.key.RIGHT:
            self.right_pressed = False
        if key == arcade.key.E:
            self.e_pressed = False

        # Update diagonal states and direction after any key release
        self.update_direction()

    def update_direction(self):
        self.diagonal_up_right = self.up_pressed and self.right_pressed
        self.diagonal_up_left = self.up_pressed and self.left_pressed
        self.diagonal_down_right = self.down_pressed and self.right_pressed
        self.diagonal_down_left = self.down_pressed and self.left_pressed

        # Calculate direction based on key combinations
        if self.diagonal_up_right:
            self.direction = 45  # Northeast
        elif self.diagonal_up_left:
            self.direction = 135  # Northwest
        elif self.diagonal_down_left:
            self.direction = 225  # Southwest
        elif self.diagonal_down_right:
            self.direction = 315  # Southeast
        elif self.right_pressed:
            self.direction = 0  # East
        elif self.up_pressed:
            self.direction = 90  # North
        elif self.left_pressed:
            self.direction = 180  # West
        elif self.down_pressed:
            self.direction = 270  # South
