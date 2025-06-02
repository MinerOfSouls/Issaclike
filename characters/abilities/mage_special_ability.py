import arcade
from arcade import PymunkPhysicsEngine
from characters.aiming_controller import AimingController
from characters.stats import Stats
from collectables.base.interactive_item import InteractiveItem
from resource_manager import get_object


class MageSpecialAbility(AimingController):
    def __init__(self, physics_engine: PymunkPhysicsEngine, stats: Stats, player_sprite: arcade.Sprite):
        super().__init__(player_sprite, stats)

        self.effects_list = arcade.SpriteList()
        self.physics_engine = physics_engine
        self.active = True
        self.stats = stats
        self.magic_shield = None

    def on_setup(self) -> None:
        shield_sprite = get_object("magic_shield")
        self.magic_shield = InteractiveItem(self.physics_engine, self.stats, shield_sprite[0], shield_sprite[1])
        self.magic_shield.position = self.player_sprite.position
        self.effects_list.append(self.magic_shield)
        self.magic_shield.on_setup()

    def __show_shield(self) -> None:
        if not self.active:
            self.active = True
            self.stats.invincible = True
            self.stats.ability_active = True
            self.effects_list.append(self.magic_shield)

    def __hide_shield(self) -> None:
        if self.active:
            self.active = False
            self.stats.invincible = False
            self.stats.ability_active = False
            self.effects_list.remove(self.magic_shield)

    def __calculate_position(self) -> None:
        self.physics_engine.set_position(self.magic_shield, self.player_sprite.position)

    def draw(self) -> None:
        self.effects_list.draw()

    def update(self) -> None:
        self.__calculate_position()
        self.effects_list.update()

    def on_key_press(self, key) -> None:
        super().on_key_press(key)
        if key == arcade.key.SPACE:
            self.__show_shield()
            self.space_pressed = True

    def on_key_release(self, key) -> None:
        super().on_key_release(key)
        if key == arcade.key.SPACE:
            self.__hide_shield()
            self.space_pressed = False
