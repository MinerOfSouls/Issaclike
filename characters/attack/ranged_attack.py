from characters.attack.attack import Attack
import arcade
import math
projectile_sprite = 'resources/images/projectile_placeholder.png'
class RangedAttack(Attack):
    def __init__(self, player_sprite,stats):
        super().__init__(player_sprite,stats)
        self.projectile_list = arcade.SpriteList()
        self.ticks = 0
        self.attack_cooldown = 0

    def update(self):
        self.ticks += 1
        self.attack_cooldown += 1

        if self.right_pressed and self.up_pressed:
            self.spawn_projectile(0 + 45)
        elif self.up_pressed and self.left_pressed:
            self.spawn_projectile(90 + 45)
        elif self.left_pressed and self.down_pressed:
            self.spawn_projectile(180 + 45)
        elif self.down_pressed and self.right_pressed:
            self.spawn_projectile(270 + 45)
        elif self.right_pressed:
            self.spawn_projectile(0)
        elif self.up_pressed:
            self.spawn_projectile(90)
        elif self.left_pressed:
            self.spawn_projectile(180)
        elif self.down_pressed:
            self.spawn_projectile(270)

        # warning fragile to framrate
        for projectile in self.projectile_list:
            if hasattr(projectile, 'range'):
                projectile.range -= 1
                if projectile.range <= 0:
                    projectile.remove_from_sprite_lists()

        self.projectile_list.update()

    # fragile to framrate
    def spawn_projectile(self, projectile_deg):
        if self.attack_cooldown < self.stats.get_projectile_cooldown():
            return
        self.attack_cooldown = 0

        projectile = arcade.Sprite(projectile_sprite, scale=0.05)

        start_x = self.player.center_x
        start_y = self.player.center_y
        projectile.center_x = start_x
        projectile.center_y = start_y

        projectile.angle = projectile_deg
        radians = math.radians(projectile_deg)
        projectile.range = self.stats.get_projectile_range()

        speed = self.stats.get_projectile_speed()

        speedx = math.sqrt(speed ** 2 + abs(self.player.change_x ** 2))
        speedy = math.sqrt(speed ** 2 + abs(self.player.change_y ** 2))

        projectile.change_x = math.cos(radians) * speedx
        projectile.change_y = math.sin(radians) * speedy

        # Add the projectile to the appropriate lists
        self.projectile_list.append(projectile)

    def on_draw(self):
        self.projectile_list.draw()