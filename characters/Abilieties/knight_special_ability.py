import math
import arcade
from characters.attack.attack import Attack
from characters.player_controller import PlayerController
from collectables.animation import Animation
from collectables.interactive_item import InteractiveItem
from resource_manager import get_object


class KnightSpecialAbility(PlayerController):
    def __init__(self, physics_engine, player_sprite, stats):
        super().__init__(player_sprite, stats)
        self.effects_list = arcade.SpriteList()
        self.physics_engine = physics_engine
        self.player_sprite = player_sprite

        # Ability configuration
        self.ability_cooldown_max = 30
        self.roll_force = 1500
        self.roll_duration = 15

        # State variables
        self.ability_active = False
        self.ability_cooldown_timer = 0
        self.roll_timer = 0


    def delete_effect_on_room_transition(self):
        self.effects_list.clear()

    def spawn_effect(self):
        dash_effect_sprite = get_object("dash_effect")
        dash_effect = Animation(
            dash_effect_sprite[0],
            dash_effect_sprite[1]
        )
        dash_effect.position = self.player_sprite.position
        # dash_effect.on_setup()
        self.effects_list.append(dash_effect)

    def calculate_roll_vector(self, target_angle_deg):
        radians = math.radians(target_angle_deg)
        return math.cos(radians), math.sin(radians)

    def start_roll(self):

        dir_x, dir_y = self.calculate_roll_vector(self.direction)
        force_x, force_y = dir_x * self.roll_force, dir_y * self.roll_force
        self.physics_engine.apply_impulse(self.player_sprite, (force_x, force_y))

        self.spawn_effect()

        self.ability_active = True
        self.stats.invincible = True
        self.roll_timer = self.roll_duration
        self.ability_cooldown_timer = self.ability_cooldown_max

    def end_roll(self):
        self.stats.invincible = False
        self.ability_active = False

    def delete_inactive_effects(self):
        for effect in self.effects_list:
            if effect.should_delete:
                self.effects_list.remove(effect)

    def draw(self):
        self.effects_list.draw()

    def update(self):
        if not self.ability_active and self.ability_cooldown_timer > 0:
            self.ability_cooldown_timer -= 1

        if self.ability_active:
            self.roll_timer -= 1
            if self.roll_timer <= 0:
                self.end_roll()

        self.delete_inactive_effects()
        self.effects_list.update()

    def on_key_press(self, key):
        super().on_key_press(key)
        if key == arcade.key.SPACE and not self.ability_active and self.ability_cooldown_timer <= 0:
            self.start_roll()