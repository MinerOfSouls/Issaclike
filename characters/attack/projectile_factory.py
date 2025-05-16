import math
from arcade import PymunkPhysicsEngine
from collectables.interactive_item import InteractiveItem
from resource_manager import get_object


class ProjectileFactory:
    def __init__(self, physics_engine, player_sprite, stats, projectile_list):
        self.physics_engine = physics_engine
        self.player_sprite = player_sprite
        self.stats = stats
        self.projectile_list = projectile_list
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

    def spawn_projectile(self, angle_deg):
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

        # Calculate direction vector
        radians = math.radians(angle_deg)
        dir_x, dir_y = math.cos(radians), math.sin(radians)

        # Offset from player center
        size = max(self.player_sprite.width, self.player_sprite.height) / 2
        projectile.center_x += dir_x * size
        projectile.center_y += dir_y * size

        # Calculate force with player momentum
        force_x, force_y = dir_x * self.stats.projectile_speed, dir_y * self.stats.projectile_speed
        p_vel_x, p_vel_y = self.physics_engine.get_physics_object(self.player_sprite).body.velocity
        force_x += p_vel_x * 0.2  # momentum_factor
        force_y += p_vel_y * 0.2

        # Launch projectile
        projectile.apply_impulse((force_x, force_y))
        self.projectile_list.append(projectile)