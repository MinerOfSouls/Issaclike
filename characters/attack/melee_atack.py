import arcade

from characters.attack.attack import Attack
from characters.sword_creator import SwordCreator
import math

class MeleeAttack(Attack):
    def __init__(self,player_sprite, physics_engine, stats):
        super().__init__(player_sprite, stats)

        self.physics_engine = physics_engine
        self.player_sprite = player_sprite

        self.sword_list = arcade.SpriteList()
        self.sword_creator = SwordCreator(self.physics_engine,self.player_sprite,self.sword_list,self.stats)
        self.sword = self.sword_creator.spawn_sword(0)

        self.degree = 0

        self.physics_engine.add_collision_handler(
            "sword",
            "player",
            post_handler=self.player_sword_handler,
        )

    def player_sword_handler(self ,sprite_a, sprite_b, arbiter, space, data):
        self.sword.held = True
        self.sword.returning = False
        print("sword collected")

    def calculate_position(self):

        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        self.sword.position = start_x, start_y
        self.sword.angle = 270 + self.degree

        radians = math.radians(self.degree)
        target = self.degree+270
        side_x = math.cos(radians)
        side_y = math.sin(radians)

        size = max(self.player_sprite.width, self.player_sprite.height) /1.7

        x= self.sword.center_x + size * side_x
        y= self.sword.center_y + size * side_y

        self.physics_engine.set_position(self.sword, (x, y))
        self.physics_engine.set_rotation(self.sword, target)

    def update(self):
        # Store the previous key state to detect release
        was_key_pressed = self.sword.charging > 0

        if (self.left_pressed or self.right_pressed or self.up_pressed or self.down_pressed) and self.sword.held:
            self.sword.charging += 1
            key_press_state = True
        else:
            key_press_state = False


        # Setting direction based on pressed keys
        if self.right_pressed and self.up_pressed:
            self.degree = 45
        elif self.up_pressed and self.left_pressed:
            self.degree = 135
        elif self.left_pressed and self.down_pressed:
            self.degree = 225
        elif self.down_pressed and self.right_pressed:
            self.degree = 315
        elif self.right_pressed:
            self.degree = 0
        elif self.up_pressed:
            self.degree = 90
        elif self.left_pressed:
            self.degree = 180
        elif self.down_pressed:
            self.degree = 270

        # Detect key release after charging
        if was_key_pressed and not key_press_state and self.sword.held:
            self.sword.held = False

            force_y = 100 * (min(self.sword.charging,self.sword.charge_time) / self.sword.charge_time)

            self.sword.apply_impulse((0, force_y))
            self.sword.charging = 0

        elif not key_press_state:
            self.sword.charging = 0

        projectile_body = self.physics_engine.get_physics_object(self.sword).body
        vel_x, vel_y = projectile_body.velocity
        vel_magnitude = math.sqrt(vel_x ** 2 + vel_y ** 2)
        min_velocity = 75.0

        if vel_magnitude < min_velocity and not self.sword.held:
            self.sword.returning = True

        if self.sword.returning and not self.sword.held:
            dx = self.player_sprite.center_x - self.sword.center_x
            dy = self.player_sprite.center_y - self.sword.center_y
            dist = math.hypot(dx, dy)


            # Normalize direction and apply return speed
            dx, dy = dx / dist, dy / dist
            self.physics_engine.set_velocity(
                self.sword,
                (dx * 500, dy * 500)
            )

        if self.sword.held:
            self.calculate_position()

        self.sword_list.update()

    def on_draw(self):
        self.sword_list.draw()

        if self.sword.charging > 0 and self.sword.held:
            charge_percentage = min(self.sword.charging / self.sword.charge_time, 1)

            r = min(255, int(charge_percentage * 255))
            g = min(255, int((1 - charge_percentage) * 255))
            b = 0

            # Set circle position to be near the player
            circle_x = self.player_sprite.center_x +20
            circle_y = self.player_sprite.center_y +20

            # Draw background circle (outline)
            arcade.draw_circle_outline(
                circle_x, circle_y,
                radius=10,
                color=(100, 100, 100),
                border_width=2
            )

            end_angle = 360 * charge_percentage

            arcade.draw_arc_filled(
                circle_x, circle_y,
                width=20,
                height=20,
                color=(r, g, b, 180),
                start_angle=0,
                end_angle=end_angle
            )

