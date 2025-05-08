from characters.attack.attack import Attack
import math
from characters.attack.projectile import Projectile


projectile_url = "resources/images/projectile_placeholder.png"
scale = 0.009



class RangedAttack(Attack):
    def __init__(self, player_sprite, physics_engine,stats):
        super().__init__(player_sprite, stats)
        self.physics_engine = physics_engine
        self.projectile = Projectile(player_sprite, stats,projectile_url,scale, physics_engine)
        self.projectile_list = self.projectile.projectile_list  # Reference the same list
        self.attack_cooldown = stats.projectile_cooldown
        self.charge_attack = 0

    def shoot_projectile(self):
        if self.attack_cooldown > self.stats.projectile_cooldown:
            if self.right_pressed and self.up_pressed:
                self.projectile.spawn_projectile(45)  # 0 + 45
                self.attack_cooldown = 0
            elif self.up_pressed and self.left_pressed:
                self.projectile.spawn_projectile(135)  # 90 + 45
                self.attack_cooldown = 0
            elif self.left_pressed and self.down_pressed:
                self.projectile.spawn_projectile(225)  # 180 + 45
                self.attack_cooldown = 0
            elif self.down_pressed and self.right_pressed:
                self.projectile.spawn_projectile(315)  # 270 + 45
                self.attack_cooldown = 0
            elif self.right_pressed:
                self.projectile.spawn_projectile(0)
                self.attack_cooldown = 0
            elif self.up_pressed:
                self.projectile.spawn_projectile(90)
                self.attack_cooldown = 0
            elif self.left_pressed:
                self.projectile.spawn_projectile(180)
                self.attack_cooldown = 0
            elif self.down_pressed:
                self.projectile.spawn_projectile(270)
                self.attack_cooldown = 0

    def delete_projectile(self):
        for projectile in self.projectile_list:
            projectile_body = self.physics_engine.get_physics_object(projectile).body
            vel_x, vel_y = projectile_body.velocity
            vel_magnitude = math.sqrt(vel_x ** 2 + vel_y ** 2)

            # If velocity is too low, remove the projectile
            min_velocity = 30.0  # Adjust this threshold as needed
            if vel_magnitude < min_velocity:
                projectile.remove_from_sprite_lists()

    def update(self):
        self.attack_cooldown += 1

        self.shoot_projectile()

        self.delete_projectile()

        # Update projectiles
        self.projectile_list.update()

    def on_draw(self):
        self.projectile_list.draw()