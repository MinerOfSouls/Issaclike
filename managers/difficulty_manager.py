import arcade

from effects.item_effects import ItemEffects
from managers.attack_manager import AttackManager
from managers.moving_fire import MovingFire
from managers.random_explosions import RandomExplosions
from managers.wind_effect import Wind


class DifficultyOptions:
    def __init__(self, physics_engine, player_sprite, stats, attack_manager, map, effects_list, difficulty_options):
        self.physics_engine = physics_engine
        self.player_sprite = player_sprite
        self.stats = stats
        self.map = map
        self.effects_list = effects_list
        self.attack_manager = attack_manager
        self.change_weapon_timout = 0
        self.difficulty_modifiers = []
        self.difficulty_options = difficulty_options

    def on_setup(self):
        modifier_constructors = {
            'wind': lambda: Wind(self.physics_engine, self.stats, self.map),
            'explosions': lambda: RandomExplosions(self.physics_engine, self.effects_list, self.stats),
            'moving_fire': lambda: MovingFire(self.physics_engine, self.player_sprite, self.effects_list, self.stats),
            'weapon_change': lambda: self.attack_manager
        }

        for modifier, enabled in self.difficulty_options.items():
            if enabled and modifier in modifier_constructors:
                self.difficulty_modifiers.append(modifier_constructors[modifier]())

        for modifier in self.difficulty_modifiers:
            modifier.on_setup()

    def draw(self):
        for modifier in self.difficulty_modifiers:
            modifier.draw()

    def update(self):
        for modifier in self.difficulty_modifiers:
            modifier.update()
