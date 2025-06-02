import arcade
import math

from arcade import PymunkPhysicsEngine

from characters.aiming_controller import AimingController
from characters.stats import Stats
from collectables.base.interactive_item import InteractiveItem  # Assuming this path is correct
from effects.charge_effect import ChargeEffects  # Assuming this path is correct
from resource_manager import get_object  # Assuming this path is correct

FULL_CHARGE = 30
MIN_VELOCITY = 75.0
RETURN_SPEED = 500
THROW_FORCE_FACTOR = 100
BOOMERANG_ROTATION_SPEED_RADS = math.pi * 16


class BoomerangAttack(AimingController):
    def __init__(self, player_sprite: arcade.Sprite, physics_engine: PymunkPhysicsEngine, stats: Stats):
        super().__init__(player_sprite, stats)

        self.physics_engine = physics_engine
        self.player_sprite = player_sprite

        self.current_charge = 0
        self.held = True
        self.returning = False
        self.thrown_time = 0

        sprite_data = get_object("boomerang")
        self.boomerang = InteractiveItem(physics_engine, stats, sprite_data[0], sprite_data[1])
        self.boomerang.on_setup()
        self.boomerang_list = arcade.SpriteList()
        self.boomerang_list.append(self.boomerang)

        # Set up collision handler
        self.physics_engine.add_collision_handler(
            "player", "boomerang",
            pre_handler=self.__player_boomerang_handler
        )

    def __player_boomerang_handler(self, sprite_a, sprite_b, arbiter, space, data) -> bool:
        if not self.held and self.thrown_time > FULL_CHARGE:
            self.thrown_time = 0
            self.held = True
            self.returning = False
            if self.physics_engine.get_physics_object(self.boomerang):
                projectile_body = self.physics_engine.get_physics_object(self.boomerang).body
                projectile_body.angular_velocity = 0
            return True
        return False

    def __calculate_position(self) -> None:
        radians = math.radians(self.direction)
        size = max(self.player_sprite.width, self.player_sprite.height) / 3

        side_x, side_y = math.cos(radians), math.sin(radians)
        x = self.player_sprite.center_x + size * side_x
        y = self.player_sprite.center_y + size * side_y
        target_angle = self.direction + 270

        self.physics_engine.set_position(self.boomerang, (x, y))
        self.physics_engine.set_rotation(self.boomerang, target_angle)

    def __attack(self) -> None:
        if not self.held:
            self.thrown_time += 1
        key_pressed = any([self.left_pressed, self.right_pressed,
                           self.up_pressed, self.down_pressed])

        self.update_direction()

        if key_pressed and self.held:
            self.current_charge += 1
        elif self.current_charge > 0 and not key_pressed and self.held:
            self.held = False
            force = THROW_FORCE_FACTOR * (min(self.current_charge, FULL_CHARGE) / FULL_CHARGE)

            self.boomerang.apply_impulse((0, force))

            if self.physics_engine.get_physics_object(self.boomerang):
                projectile_body = self.physics_engine.get_physics_object(self.boomerang).body
                projectile_body.angular_velocity = BOOMERANG_ROTATION_SPEED_RADS

            self.current_charge = 0
        elif not key_pressed:
            self.current_charge = 0

        if not self.held:
            projectile_body = self.physics_engine.get_physics_object(self.boomerang).body
            vel_x, vel_y = projectile_body.velocity
            if math.hypot(vel_x,
                          vel_y) < MIN_VELOCITY and not self.returning:
                self.returning = True

            if self.returning:
                dx = self.player_sprite.center_x - self.boomerang.center_x
                dy = self.player_sprite.center_y - self.boomerang.center_y
                dist = math.hypot(dx, dy)

                if dist > 0:
                    self.physics_engine.set_velocity(
                        self.boomerang,
                        (dx / dist * RETURN_SPEED, dy / dist * RETURN_SPEED)
                    )
        else:
            self.__calculate_position()
        self.boomerang_list.update()

    def update(self) -> None:
        if not self.stats.ability_active:
            self.__attack()

    def on_draw(self) -> None:
        self.boomerang_list.draw()
        if self.held and self.current_charge > 0:
            ChargeEffects.charge_circle(self.player_sprite, self.current_charge, FULL_CHARGE)

    def reset_keys(self) -> None:
        super().reset_keys()
        self.current_charge = 0

        if not self.held and self.boomerang and self.physics_engine.get_physics_object(self.boomerang):
            projectile_body = self.physics_engine.get_physics_object(self.boomerang).body
            projectile_body.angular_velocity = 0

        self.held = True
        self.returning = False
