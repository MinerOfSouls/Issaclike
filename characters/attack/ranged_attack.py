import arcade
from arcade import PymunkPhysicsEngine

from characters.aiming_controller import AimingController
import math
from characters.attack.projectile_factory import ProjectileFactory
from characters.stats import Stats


class RangedAttack(AimingController):
    def __init__(self, player_sprite: arcade.Sprite, physics_engine: PymunkPhysicsEngine, stats: Stats):
        super().__init__(player_sprite, stats)
        self.physics_engine = physics_engine
        self.projectile_list = arcade.SpriteList()
        self.projectile = ProjectileFactory(physics_engine, player_sprite, stats, self.projectile_list)
        self.attack_cooldown = stats.projectile_cooldown

    def __shoot_projectile(self) -> None:
        key_pressed = any([self.left_pressed, self.right_pressed,
                           self.up_pressed, self.down_pressed])

        if (self.attack_cooldown > self.stats.projectile_cooldown) and key_pressed:
            self.update_direction()
            self.projectile.spawn_projectile(self.direction)
            self.attack_cooldown = 0

    def __delete_projectile(self) -> None:
        for projectile in self.projectile_list:
            projectile_body = self.physics_engine.get_physics_object(projectile).body
            vel_x, vel_y = projectile_body.velocity
            vel_magnitude = math.sqrt(vel_x ** 2 + vel_y ** 2)

            # If velocity is too low, remove the projectile
            min_velocity = 30.0
            if vel_magnitude < min_velocity:
                projectile.remove_from_sprite_lists()

    def __attack(self) -> None:
        self.attack_cooldown += 1
        self.__shoot_projectile()
        self.__delete_projectile()
        self.projectile_list.update()

    def update(self) -> None:
        if not self.stats.ability_active:
            self.__attack()

    def on_draw(self) -> None:
        self.projectile_list.draw()
