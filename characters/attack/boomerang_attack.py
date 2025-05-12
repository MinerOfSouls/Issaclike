import arcade
import math
from characters.attack.attack import Attack
from collectables.interactive_item import InteractiveItem
from effects.charge_effect import ChargeEffects
from resource_manager import get_object

# Moved constants outside the class for cleaner code
BOOMERANG_IMAGE = 'resources/images/sword.png'
BOOMERANG_CONFIG = {
    "width": 32, "height": 32, "columns": 11, "count": 11,
    "speed": 0.3, "scale": 1.5, "looping": True,
    "collectable": False, "item_type": "boomerang",
}
FULL_CHARGE = 30
MIN_VELOCITY = 75.0
RETURN_SPEED = 500
THROW_FORCE_FACTOR = 100


class BoomerangAttack(Attack):
    def __init__(self, player_sprite, physics_engine, stats):
        super().__init__(player_sprite, stats)
        self.physics_engine = physics_engine
        self.player_sprite = player_sprite

        self.current_charge = 0
        self.held = True
        self.returning = False

        # Create boomerang sprite
        sprite = get_object("boomerang")
        self.boomerang = InteractiveItem(physics_engine, stats, sprite[0], sprite[1])
        self.boomerang.on_setup()
        self.boomerang_list = arcade.SpriteList()
        self.boomerang_list.append(self.boomerang)

        # Set up collision handler
        self.physics_engine.add_collision_handler(
            "player", "boomerang",
            pre_handler=self.player_boomerang_handler
        )

    def player_boomerang_handler(self, sprite_a, sprite_b, arbiter, space, data):
        if not self.held:
            self.held = True
            self.returning = False
            return True
        return False

    def calculate_position(self):
        # Position boomerang relative to player
        radians = math.radians(self.direction)
        size = max(self.player_sprite.width, self.player_sprite.height) / 1.7

        # Calculate offset position and rotation
        side_x, side_y = math.cos(radians), math.sin(radians)
        x = self.player_sprite.center_x + size * side_x
        y = self.player_sprite.center_y + size * side_y
        target_angle = self.direction + 270

        # Update physics object
        self.physics_engine.set_position(self.boomerang, (x, y))
        self.physics_engine.set_rotation(self.boomerang, target_angle)

    def update(self):
        # Handle key press state
        key_pressed = any([self.left_pressed, self.right_pressed,
                           self.up_pressed, self.down_pressed])

        # Update direction based on pressed keys
        self.update_direction()

        # Handle charging and throwing
        if key_pressed and self.held:
            self.current_charge += 1
        elif self.current_charge > 0 and not key_pressed and self.held:
            self.held = False
            force = THROW_FORCE_FACTOR * (min(self.current_charge, FULL_CHARGE) / FULL_CHARGE)
            self.boomerang.apply_impulse((0, force))
            self.current_charge = 0
        elif not key_pressed:
            self.current_charge = 0

        # Handle boomerang movement
        if not self.held:
            projectile_body = self.physics_engine.get_physics_object(self.boomerang).body
            vel_x, vel_y = projectile_body.velocity
            if math.hypot(vel_x, vel_y) < MIN_VELOCITY:
                self.returning = True

            # Return boomerang to player
            if self.returning:
                dx = self.player_sprite.center_x - self.boomerang.center_x
                dy = self.player_sprite.center_y - self.boomerang.center_y
                dist = math.hypot(dx, dy)

                # Normalize direction and apply return speed
                if dist > 0:  # Prevent division by zero
                    self.physics_engine.set_velocity(
                        self.boomerang,
                        (dx / dist * RETURN_SPEED, dy / dist * RETURN_SPEED)
                    )
        else:
            # Update position when held
            self.calculate_position()

        # Update sprite animations
        self.boomerang_list.update()

    def on_draw(self):
        self.boomerang_list.draw()
        if self.held and self.current_charge > 0:
            ChargeEffects.charge_circle(self.player_sprite, self.current_charge, FULL_CHARGE)