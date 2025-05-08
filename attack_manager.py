from characters.attack.projectile import Projectile
from characters.attack.ranged_attack import RangedAttack
from characters.attack.melee_atack import MeleeAttack
from characters.attack.melee_attack2 import SwordSwing
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

        self.sword = SwordSwing(self.player_sprite, self.physics_engine, self.stats)
        self.boomerang = MeleeAttack(self.player_sprite, self.physics_engine, self.stats)
        self.ranged_attack = RangedAttack(self.player_sprite, self.physics_engine, self.stats)

        self.set_attack_type(AttackType.BOOMERANG)

    def set_attack_type(self, attack_type: AttackType):
        if attack_type == AttackType.SWORD:
            self.current_attack = SwordSwing(self.player_sprite, self.physics_engine, self.stats)
        elif attack_type == AttackType.BOOMERANG:
            self.current_attack = MeleeAttack(self.player_sprite, self.physics_engine, self.stats)
        elif attack_type == AttackType.RANGED:
            self.current_attack = RangedAttack(self.player_sprite, self.physics_engine, self.stats)
        else:
            raise ValueError(f"Unknown attack type: {attack_type}")

    def set_random_attack(self):
        attack_type = choice(list(AttackType))
        self.set_attack_type(attack_type)