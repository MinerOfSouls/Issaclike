from characters.attack.projectile_factory import ProjectileFactory
from characters.attack.ranged_attack import RangedAttack
from characters.attack.boomerang_attack import BoomerangAttack
from characters.attack.sword_attack import SwordSwing
from random import randint, choice

from enum import Enum, auto
class AttackType(Enum):
    SWORD = auto()
    BOOMERANG = auto()
    RANGED = auto()

class AttackManager:
    def __init__(self, physics_engine, player_sprite, stats):
        self.player_sprite = player_sprite
        self.physics_engine = physics_engine
        self.stats = stats
        self.current_attack = None
        self.change_weapon_timout = 0

        self.sword = SwordSwing(self.player_sprite, self.physics_engine, self.stats)
        self.boomerang = BoomerangAttack(self.player_sprite, self.physics_engine, self.stats)
        self.ranged_attack = RangedAttack(self.player_sprite, self.physics_engine, self.stats)

        self.set_attack_type(AttackType.SWORD)

    def on_setup(self):
        pass

    def set_attack_type(self, attack_type: AttackType):
        if attack_type == AttackType.SWORD:
            self.current_attack = self.sword
        elif attack_type == AttackType.BOOMERANG:
            self.current_attack = self.boomerang
        elif attack_type == AttackType.RANGED:
            self.current_attack = self.ranged_attack
        else:
            raise ValueError(f"Unknown attack type: {attack_type}")
        self.current_attack.reset_keys()

    def set_random_attack(self):
        attack_type = choice(list(AttackType))
        self.set_attack_type(attack_type)

    def draw(self):
        pass

    def update(self):
        self.change_weapon_timout+=1
        if self.change_weapon_timout >= 300:
            self.set_random_attack()
            self.change_weapon_timout =0