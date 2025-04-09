import arcade
import math

projectile_sprite = 'resources/images/projectile_placeholder.png'

class Attack:
    def __init__(self, player_sprite,stats):
        self.player = player_sprite
        self.stats = stats
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.projectile_list = arcade.SpriteList()
        self.ticks = 0
        self.attack_cooldown = 0

    def update(self):
        self.ticks += 1
        self.attack_cooldown +=1

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

    def on_key_press(self, key):
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
    
    def on_key_release(self, key):
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    #fragile to framrate
    def spawn_projectile(self, projectile_deg):
        if self.attack_cooldown < self.stats.get_projectile_cooldown():
            return
        self.attack_cooldown = 0

        projectile = arcade.Sprite(projectile_sprite, scale = 0.05)

        start_x = self.player.center_x
        start_y = self.player.center_y
        projectile.center_x = start_x
        projectile.center_y = start_y

        projectile.angle = projectile_deg
        projectile.range = self.stats.get_projectile_range()

        speed = self.stats.get_projectile_speed()
        radians = math.radians(projectile_deg)

        projectile.change_x = math.cos(radians) * speed
        projectile.change_y = math.sin(radians) * speed

        # Add the projectile to the appropriate lists
        self.projectile_list.append(projectile)

    def on_draw(self):
        self.projectile_list.draw()





