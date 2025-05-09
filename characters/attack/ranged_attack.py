import arcade
from characters.attack.attack import Attack
import math
from characters.attack.projectile_factory import ProjectileFactory

bomb_url = "resources/images/granade.png"
bomb_details = {
    "width": 13,
    "height": 16,
    "columns": 1,
    "count": 1,
    "speed": 0.05,
    "scale": 0.5,
    "looping": False,
    "item_type": "projectile",
}

class RangedAttack(Attack):
    def __init__(self, player_sprite, physics_engine,stats):
        super().__init__(player_sprite, stats)
        self.physics_engine = physics_engine
        self.projectile_list = arcade.SpriteList()
        self.projectile = ProjectileFactory(physics_engine,player_sprite, stats, bomb_url, bomb_details,self.projectile_list)
        self.attack_cooldown = stats.projectile_cooldown

    def shoot_projectile(self):
        key_pressed = any([self.left_pressed, self.right_pressed,
                           self.up_pressed, self.down_pressed])

        if (self.attack_cooldown > self.stats.projectile_cooldown) and key_pressed:
            self.update_direction()
            self.projectile.spawn_projectile(self.direction)
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