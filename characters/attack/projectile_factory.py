import math
import random

from arcade import PymunkPhysicsEngine
from collectables.interactive_item import InteractiveItem
from resource_manager import get_object


class ProjectileFactory:
    def __init__(self, physics_engine, player_sprite, stats, projectile_list):
        self.physics_engine = physics_engine
        self.player_sprite = player_sprite
        self.stats = stats
        self.projectile_list = projectile_list
        self.inaccuracy_degrees = 0
        sprite = get_object("projectile")
        self.projectile_url = sprite[0]
        self.projectile_details = sprite[1]

        # Set up wall collision handler
        self.physics_engine.add_collision_handler(
            "projectile", "wall",
            post_handler=lambda s_a, s_b, arb, *_: self._handle_wall_collision(arb)
        )

    def _handle_wall_collision(self, arbiter):
        """Handle projectile-wall collisions"""
        bullet_sprite = self.physics_engine.get_sprite_for_shape(arbiter.shapes[0])
        bullet_sprite.remove_from_sprite_lists()
        print("Wall")

    def spawn_projectile(self, target_angle_deg):
        # Create and position projectile
        projectile = InteractiveItem(
            self.physics_engine,
            self.stats,
            self.projectile_url,
            self.projectile_details
        )
        projectile.center_x = self.player_sprite.center_x
        projectile.center_y = self.player_sprite.center_y
        projectile.on_setup()


        if self.inaccuracy_degrees > 0:
            angle_offset = random.uniform(-self.inaccuracy_degrees / 2.0, self.inaccuracy_degrees / 2.0)
            actual_fire_angle_deg = target_angle_deg + angle_offset
        else:
            actual_fire_angle_deg = target_angle_deg

        # Calculate direction vector
        radians = math.radians(actual_fire_angle_deg)
        dir_x, dir_y = math.cos(radians), math.sin(radians)

        size = max(self.player_sprite.width, self.player_sprite.height) / 2
        spawn_offset_distance = size + 5
        projectile.center_x += dir_x * spawn_offset_distance
        projectile.center_y += dir_y * spawn_offset_distance

        force_x, force_y = dir_x * self.stats.projectile_speed, dir_y * self.stats.projectile_speed

        player_physics_object = self.physics_engine.get_physics_object(self.player_sprite)
        if player_physics_object and player_physics_object.body:
            p_vel_x, p_vel_y = player_physics_object.body.velocity
            momentum_factor = 0.2
            force_x += p_vel_x * momentum_factor
            force_y += p_vel_y * momentum_factor

        projectile.apply_impulse((force_x, force_y))
        self.projectile_list.append(projectile)