import arcade
import math
from arcade import PymunkPhysicsEngine
from characters.attack.attack import Attack
from resource_manager import get_object

class SwordSwing(Attack):
    def __init__(self, player_sprite, physics_engine, stats):
        super().__init__(player_sprite, stats)
        self.physics_engine = physics_engine
        self.sword_list = arcade.SpriteList()
        self.sword = None
        self.is_swinging = False
        self.swing_angle = 0
        self.timeout = 20

        # Constants
        self.sword_length = 50
        self.swing_speed = 10
        self.swing_range = 180

    def _create_sword(self):
        """Create and setup sword sprite"""
        self.sword = arcade.Sprite(get_object("sword"), scale=1.5)
        self.sword_list.append(self.sword)

        self.physics_engine.add_sprite(
            self.sword,
            mass=10.0,
            body_type=PymunkPhysicsEngine.KINEMATIC,
            collision_type="sword",
            elasticity=0.5
        )

        self.physics_engine.add_collision_handler(
            "sword", "player",
            pre_handler=lambda *_: False  # Prevent player-sword collisions
        )

        self.swing_angle = -self.swing_range / 2
        self.is_swinging = True

    def _update_sword_position(self):
        """Update sword position based on swing progress"""
        pivot_x, pivot_y = self.player.center_x, self.player.center_y
        current_angle = self.direction + self.swing_angle
        angle_rad = math.radians(current_angle)

        # Position sword center relative to pivot point
        sword_x = pivot_x + (self.sword_length / 2) * math.cos(angle_rad)
        sword_y = pivot_y + (self.sword_length / 2) * math.sin(angle_rad)

        self.physics_engine.set_position(self.sword, (sword_x, sword_y))
        self.physics_engine.set_rotation(self.sword, current_angle)

    def _end_swing(self):
        """Clean up after swing completes"""
        if self.sword:
            self.physics_engine.remove_sprite(self.sword)
            self.sword_list.clear()
            self.sword = None
        self.is_swinging = False

    def on_key_press(self, key):
        super().on_key_press(key)
        if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT):
            if not self.is_swinging and self.timeout >= 20:
                self._create_sword()
                self.timeout = 0

    def attack(self):
        self.timeout += 1

        # Update facing direction
        self.update_direction()

        # Handle swing animation
        if self.is_swinging:
            self.swing_angle += self.swing_speed
            self._update_sword_position()
            if self.swing_angle >= self.swing_range / 2:
                self._end_swing()
        self.sword_list.update()

    def update(self):
        if not self.stats.ability_active:
            self.attack()
        elif self.is_swinging:
            self._end_swing()


    def on_draw(self):
        self.sword_list.draw()