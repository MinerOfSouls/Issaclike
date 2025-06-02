import random
import arcade
from arcade import PymunkPhysicsEngine

from characters.aiming_controller import AimingController
from characters.attack.projectile_factory import ProjectileFactory
from characters.stats import Stats
from resource_manager import get_object

ABILITY_DURATION = 300
ABILITY_COOLDOWN = 600
SHOOT_INTERVAL = 5


class DragonSpecialAbility(AimingController):
    def __init__(self, physics_engine: PymunkPhysicsEngine, player_sprite: arcade.Sprite, stats: Stats):
        super().__init__(player_sprite, stats)

        self.effects_list = arcade.SpriteList()
        self.physics_engine = physics_engine

        self.projectile_factory = ProjectileFactory(physics_engine, player_sprite, stats, self.effects_list)
        self.projectile_factory.inaccuracy_degrees = 45

        sprite = get_object("shoot_fire")
        self.projectile_factory.projectile_url = sprite[0]
        self.projectile_factory.projectile_details = sprite[1]

        self.ability_active = False
        self.ability_timer = 0
        self.ability_cooldown_timer = 0
        self.shoot_counter = 0

    def __shoot_fire(self) -> None:
        self.update_direction()
        self.projectile_factory.projectile_details["scale"] = random.uniform(0.025, 0.1)
        self.projectile_factory.spawn_projectile(self.direction)

    def __delete_fire(self) -> None:
        for fire in self.effects_list:
            if fire.item_lifetime > 200:
                self.effects_list.remove(fire)
                self.physics_engine.remove_sprite(fire)

    def delete_effect_on_room_transition(self) -> None:
        for effect in self.effects_list:
            self.physics_engine.remove_sprite(effect)
            self.effects_list.remove(effect)

    def draw(self) -> None:
        self.effects_list.draw()

    def update(self) -> None:
        if not self.ability_active and self.ability_cooldown_timer > 0:
            self.ability_cooldown_timer -= 1

        if self.ability_active:
            self.ability_timer -= 1
            self.shoot_counter -= 1

            if self.shoot_counter <= 0:
                self.__shoot_fire()
                self.shoot_counter = SHOOT_INTERVAL

            if self.ability_timer <= 0:
                self.ability_active = False
                self.stats.ability_active = False
                self.ability_cooldown_timer = ABILITY_COOLDOWN

        self.__delete_fire()
        self.effects_list.update()

    def on_key_press(self, key) -> None:
        super().on_key_press(key)
        if key == arcade.key.SPACE and not self.ability_active and self.ability_cooldown_timer <= 0:
            self.ability_active = True
            self.stats.ability_active = True
            self.ability_timer = ABILITY_DURATION
            self.shoot_counter = 0
