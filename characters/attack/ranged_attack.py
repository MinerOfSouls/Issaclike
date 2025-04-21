from types import NoneType

from arcade import PymunkPhysicsEngine

from characters.attack.attack import Attack
import arcade
import math
PROJECTILE_SPRITE = 'resources/images/projectile_placeholder.png'
class RangedAttack(Attack):
    def __init__(self, player_sprite, stats, engine: PymunkPhysicsEngine):
        super().__init__(player_sprite,stats)
        self.projectile_list = arcade.SpriteList()
        self.ticks = 0
        self.attack_cooldown = 0
        self.engine = engine
        self.id = 0

        def projectile_wall_collision(projectile, *args):
            try:
                projectile.remove_from_sprite_lists()
            except AttributeError:
                #ignored
                pass
            return False

        self.engine.add_collision_handler("player_projectile", "wall", pre_handler=projectile_wall_collision)
        self.engine.add_collision_handler("player_projectile", "door", pre_handler=projectile_wall_collision)
        #no player collision
        def no_collision(*args):
            return False
        self.engine.add_collision_handler("player_projectile", "player", pre_handler=no_collision)
        self.engine.add_collision_handler("player_projectile", "player_projectile", pre_handler=no_collision)

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

        for s in self.projectile_list:
            self.engine.apply_force(s, s.properties["force"])

        self.projectile_list.update()

    # fragile to framrate
    def spawn_projectile(self, projectile_deg):
        if self.attack_cooldown < self.stats.get_projectile_cooldown():
            return
        self.attack_cooldown = 0

        projectile = arcade.Sprite(PROJECTILE_SPRITE, scale=0.03)
        projectile.properties["id"] = self.id

        start_x = self.player.center_x
        start_y = self.player.center_y
        projectile.center_x = start_x
        projectile.center_y = start_y

        speed = self.stats.get_projectile_speed()

        speedx = math.sqrt(speed ** 2 + abs(self.player.change_x ** 2))
        speedy = math.sqrt(speed ** 2 + abs(self.player.change_y ** 2))

        self.engine.add_sprite(
            projectile,
            mass = 0.01,
            moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
            collision_type="player_projectile",
            damping=0,
            body_type=0,
        )
        self.engine.set_rotation(projectile, projectile_deg)
        self.engine.apply_force(projectile, (10*speedx, 10*speedy))
        projectile.properties["force"] = (10*speedx, 10*speedy)

        # Add the projectile to the appropriate lists
        self.projectile_list.append(projectile)

        self.id += 1

    def on_draw(self):
        self.projectile_list.draw()