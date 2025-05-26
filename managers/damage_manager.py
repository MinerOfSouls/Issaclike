# damage manager singleton
from effects.charge_effect import ChargeEffects


class DamageManager:
    _instance = None
    def __new__(cls, stats=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            if stats is not None:
                cls._instance.stats = stats
                cls._instance.invulnerability_frames = 0
        return cls._instance

    def deal_damage(self, target_stats=None):
        stats = target_stats or self.stats
        if self.invulnerability_frames >= 60 and stats.health > 0  and  not self.stats.invincible:
            print("damage_taken")
            stats.health -= 1
            self._instance.invulnerability_frames = 0

    def update(self):
        self._instance.invulnerability_frames += 1