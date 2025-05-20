import random

import arcade
from characters.attack.attack import Attack
from characters.attack.projectile_factory import ProjectileFactory
from resource_manager import get_object


class DragonSpecialAbility(Attack):
    def __init__(self, physics_engine, player_sprite, stats,effect_list):
        super().__init__(player_sprite, stats)
        self.effects_list = arcade.SpriteList()
        self.physics_engine = physics_engine
        self.projectile_factory = ProjectileFactory(physics_engine, player_sprite, stats, self.effects_list)
        self.projectile_factory.inaccuracy_degrees = 45
        sprite = get_object("shoot_fire")
        self.projectile_factory.projectile_url = sprite[0]
        self.projectile_factory.projectile_details = sprite[1]

        self.ability_duration = 300
        self.ability_cooldown_max = 600
        self.shoot_interval = 5

        self.ability_active = False
        self.ability_timer = 0
        self.ability_cooldown_timer = 0
        self.shoot_counter = 0

    def delete_effect_on_room_transition(self):
        self.effects_list.clear()
        for effect in self.effects_list:
            self.physics_engine.remove_sprite(effect)

    def shoot_fire(self):
        self.update_direction()
        self.projectile_factory.projectile_details["scale"] = random.uniform(0.025,0.1)
        self.projectile_factory.spawn_projectile(self.direction)

    def delete_fire(self):
        for fire in self.effects_list:
            if fire.item_lifetime > 300:
                self.effects_list.remove(fire)
                self.physics_engine.remove_sprite(fire)

    def draw(self):
        self.effects_list.draw()

    def update(self):
        if not self.ability_active and self.ability_cooldown_timer > 0:
            self.ability_cooldown_timer -= 1

        if self.ability_active:
            self.ability_timer -= 1
            self.shoot_counter -= 1

            if self.shoot_counter <= 0:
                self.shoot_fire()
                self.shoot_counter = self.shoot_interval

            if self.ability_timer <= 0:
                self.ability_active = False
                self.stats.ability_active = False
                self.ability_cooldown_timer = self.ability_cooldown_max

        self.delete_fire()
        self.effects_list.update()

    def on_key_press(self, key):
        super().on_key_press(key)
        if key == arcade.key.SPACE and not self.ability_active and self.ability_cooldown_timer <= 0:
            self.ability_active = True
            self.stats.ability_active = True
            self.ability_timer = self.ability_duration
            self.shoot_counter = 0