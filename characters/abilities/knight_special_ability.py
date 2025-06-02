import math
import arcade
from arcade import PymunkPhysicsEngine

from characters.player_controller import PlayerController
from characters.stats import Stats
from collectables.base.animation import Animation
from resource_manager import get_object

ABILITY_COOLDOWN = 30
DASH_FORCE = 1500
DASH_DURATION = 30


class KnightSpecialAbility(PlayerController):
    def __init__(self, physics_engine: PymunkPhysicsEngine, player_sprite: arcade.Sprite, stats: Stats):
        super().__init__(player_sprite, stats)

        self.effects_list = arcade.SpriteList()
        self.physics_engine = physics_engine
        self.player_sprite = player_sprite

        self.ability_active = False
        self.ability_cooldown_timer = 0
        self.dash_timer = 0

    def __spawn_effect(self) -> None:
        dash_effect_sprite = get_object("dash_effect")
        dash_effect = Animation(dash_effect_sprite[0], dash_effect_sprite[1])
        dash_effect.position = self.player_sprite.position
        self.effects_list.append(dash_effect)

    def __start_dash(self) -> None:
        dir_x, dir_y = math.cos(math.radians(self.direction)), math.sin(math.radians(self.direction))
        force_x, force_y = dir_x * DASH_FORCE, dir_y * DASH_FORCE

        self.physics_engine.apply_impulse(self.player_sprite, (force_x, force_y))
        self.__spawn_effect()
        self.ability_active = True
        self.stats.invincible = True
        self.dash_timer = 0
        self.ability_cooldown_timer = ABILITY_COOLDOWN

    def __end_dash(self) -> None:
        self.stats.invincible = False
        self.ability_active = False

    def __delete_inactive_effects(self) -> None:
        for effect in self.effects_list:
            if effect.should_delete:
                self.effects_list.remove(effect)

    def delete_effect_on_room_transition(self) -> None:
        self.effects_list.clear()

    def draw(self) -> None:
        self.effects_list.draw()

    def update(self) -> None:
        if not self.ability_active and self.ability_cooldown_timer > 0:
            self.ability_cooldown_timer -= 1

        if self.ability_active:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.__end_dash()

        self.__delete_inactive_effects()
        self.effects_list.update()

    def on_key_press(self, key) -> None:
        super().on_key_press(key)
        if key == arcade.key.SPACE and not self.ability_active and self.ability_cooldown_timer <= 0:
            self.__start_dash()
