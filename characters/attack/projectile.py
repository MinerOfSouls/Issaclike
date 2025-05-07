from arcade import PymunkPhysicsEngine
import arcade
import math


class Projectile(arcade.Sprite):
    def __init__(self, player_sprite, stats,projectile_url,scale, physics_engine: PymunkPhysicsEngine):
        super().__init__()
        self.player_sprite = player_sprite
        self.stats = stats
        self.physics_engine = physics_engine
        self.projectile_list = arcade.SpriteList()
        self.projectile_url = projectile_url
        self.scale = scale


        def wall_hit_handler(sprite_a, sprite_b, arbiter, space, data):
            """ Called for bullet/rock collision """
            bullet_shape = arbiter.shapes[0]
            bullet_sprite = self.physics_engine.get_sprite_for_shape(bullet_shape)
            bullet_sprite.remove_from_sprite_lists()
            print("Wall")

        self.physics_engine.add_collision_handler(
            "projectile",
            "wall",
            post_handler=wall_hit_handler,
        )

    def spawn_projectile(self, projectile_deg):
        projectile = arcade.Sprite(self.projectile_url, self.scale)

        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        projectile.center_x = start_x
        projectile.center_y = start_y


        radians = math.radians(projectile_deg)

        # Calculate force direction based on angle
        force_x = math.cos(radians)
        force_y = math.sin(radians)

        size = max(self.player_sprite.width, self.player_sprite.height) / 2

        projectile.center_x += size * force_x
        projectile.center_y += size * force_y

        self.physics_engine.add_sprite(projectile,
                                       mass=0.1,
                                       damping=0.01,
                                       friction=0.3,
                                       body_type=PymunkPhysicsEngine.DYNAMIC,
                                       collision_type="projectile",
                                       elasticity=0.9)

        # Apply force with appropriate magnitude
        speed = self.stats.projectile_speed
        force_x *= speed
        force_y *= speed

        # Get player's current velocity
        player_body = self.physics_engine.get_physics_object(self.player_sprite).body
        player_vel_x, player_vel_y = player_body.velocity

        # Add player's velocity to the projectile force (momentum transfer)
        # You can adjust the momentum_factor to control how much of the player's momentum transfers
        momentum_factor = 0.2
        force_x += player_vel_x * momentum_factor
        force_y += player_vel_y * momentum_factor

        # Apply the impulse to the projectile
        self.physics_engine.apply_impulse(projectile, (force_x, force_y))

        # Add the projectile to the sprite list
        self.projectile_list.append(projectile)

        return projectile

