import arcade

from characters.Abilieties.special_ability import SpecialAbility
from collectables.interactive_item import InteractiveItem
from resource_manager import get_object

# loaded is currently a bypass some bug with key press
class MageSpecialAbility(SpecialAbility):
    def __init__(self,physics_engine,stats,player_sprite):
        super().__init__(player_sprite)
        self.shield_list = arcade.SpriteList()
        self.physics_engine = physics_engine
        self.loaded = False
        self.active = True
        self.stats = stats
        self.magic_shield = None


    def on_setup(self):
        shield_sprite = get_object("magic_shield")
        self.magic_shield = InteractiveItem(self.physics_engine, self.stats, shield_sprite[0], shield_sprite[1])
        self.magic_shield.position = self.player_sprite.position
        self.shield_list.append(self.magic_shield)
        self.magic_shield.on_setup()
        self.loaded = True


    def show_shield(self):
        if not self.active:
            self.active = True
            self.stats.invincible = True
            self.stats.ability_active = True
            self.shield_list.append(self.magic_shield)

    def hide_shield(self):
        if self.active:
            self.active = False
            self.stats.invincible = False
            self.stats.ability_active = False
            self.shield_list.remove(self.magic_shield)

    def calculate_position(self):
        self.physics_engine.set_position(self.magic_shield, self.player_sprite.position)

    def draw(self):
        self.shield_list.draw()

    def update(self):
        self.calculate_position()
        self.shield_list.update()

    def on_key_press(self, key):
        super().on_key_press(key)
        if key == arcade.key.SPACE and self.loaded:
            self.show_shield()
            self.space_pressed = True

    def on_key_release(self, key):
        super().on_key_release(key)
        if key == arcade.key.SPACE and self.loaded:
            self.hide_shield()
            self.space_pressed = False