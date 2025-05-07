import arcade
from arcade import PymunkPhysicsEngine
import math

from characters.attack.attack import Attack


# todo rewrite split logic between sword this only controlls and inicialse sword

class SwordSwing(Attack):
    def __init__(self, player_sprite, physics_engine, stats):
        super().__init__(player_sprite, stats)
        
        self.physics_engine = physics_engine
        self.pivot_offset = 1 # Distance from player center to sword handle/pivot point
        self.sword_length = 50  # Length of the sword from handle to tip
        self.handle_position = (0, 0)

        # Sword properties
        self.sword_list = arcade.SpriteList()
        self.sword_image_path = 'resources/images/swords1.png'
        self.sword = None
        self.facing_degree = 0
        self.timeout = 20

        self.sword_reach = max(self.player.width, self.player.height) / 5

        self.is_swinging = False
        self.swing_angle = 0  # Current progress of swing (-90 to 90 degrees)
        self.swing_speed = 10  # Degrees per frame
        self.swing_range = 180  # Total swing arc in degrees

        self.sword_pivot_joint =None

        # Charging attack properties
        self.is_charging = False
        self.charge_time = 0

    def player_sword_handler(self, sprite_a, sprite_b, arbiter, space, data):
        """Prevent collision between player and their sword"""
        return False

    def create_sword(self):
        """Create the sword sprite and add it to the physics engine"""
        if self.sword is not None:
            # Clean up existing sword first
            self.physics_engine.remove_sprite(self.sword)
            self.sword_list.remove(self.sword)

        self.sword = arcade.Sprite(self.sword_image_path, scale=1.5)
        self.sword_list.append(self.sword)

        # Add physics properties - using KINEMATIC for controlled movement
        self.physics_engine.add_sprite(
            self.sword,
            mass=10.0,
            body_type=PymunkPhysicsEngine.KINEMATIC,  # KINEMATIC for controlled movement
            collision_type="sword",
            elasticity=0.5  # No bounce
        )

        # Add collision handler
        self.physics_engine.add_collision_handler(
            "sword", "player",
            pre_handler=self.player_sword_handler
        )

        # Start at beginning of swing arc (-90 degrees relative to facing)
        self.swing_angle = -self.swing_range / 2
        self.is_swinging = True


    def update_swing(self):
        """Update the sword swing animation"""
        if not self.is_swinging or not self.sword:
            return

        # Advance swing progress
        self.swing_angle += self.swing_speed

        # Calculate sword position based on player position and swing angle
        self.update_sword_position()

        # Check if swing is complete
        if self.swing_angle >= self.swing_range / 2:
            self.end_swing()

    def update_sword_position(self):
        """Update the sword position based on a pivot point that stays fixed relative to player"""
        if not self.sword:
            return

        # Calculate the fixed pivot/handle position relative to player
        pivot_x = self.player.center_x
        pivot_y = self.player.center_y

        # Store handle position for collision detection or visual effects
        self.handle_position = (pivot_x, pivot_y)

        current_angle = self.facing_degree + self.swing_angle
        blade_angle_rad = math.radians(current_angle)

        # Calculate sword center position based on the handle position and half the sword length
        # (since the sprite's center is what we're positioning)
        sword_center_x = pivot_x + (self.sword_length / 2) * math.cos(blade_angle_rad)
        sword_center_y = pivot_y + (self.sword_length / 2) * math.sin(blade_angle_rad)

        # Update sword position and rotation in physics engine
        self.physics_engine.set_position(self.sword, (sword_center_x, sword_center_y))
        self.physics_engine.set_rotation(self.sword, current_angle)

    def end_swing(self):
        """End the sword swing animation and clean up"""
        self.is_swinging = False
        if self.sword:
            self.physics_engine.remove_sprite(self.sword)
            self.sword_list.clear()
            self.sword = None

    def on_key_press(self, key):
        super().on_key_press(key)
        if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT) and not self.is_swinging and self.timeout >=20:
            self.create_sword()
            self.timeout =0

    def update(self):
        self.timeout+=1
        if self.right_pressed:
            self.facing_degree = 0
        elif self.up_pressed:
            self.facing_degree = 90
        elif self.left_pressed:
            self.facing_degree = 180
        elif self.down_pressed:
            self.facing_degree = 270

        self.update_swing()

        self.sword_list.update()

    def on_draw(self):
        """Draw the sword"""
        self.sword_list.draw()
