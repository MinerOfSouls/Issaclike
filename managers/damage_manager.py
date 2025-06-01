from effects.charge_effect import ChargeEffects


class DamageManager:
    _instance = None

    def __new__(cls, stats=None, player_sprite=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Initialize only once
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, stats=None, player_sprite=None):
        if not self._initialized:
            self.stats = stats
            self.player_sprite = player_sprite
            self.invulnerability_frames = 0
            self._initialized = True

    def deal_damage(self, damage):
        if (self.invulnerability_frames >= 90 and
                self.stats.health > 0 and
                not self.stats.invincible):
            print("damage_taken")
            ChargeEffects.hit_effect(self.player_sprite)
            self.stats.health -= damage
            self.invulnerability_frames = 0

    def update(self):
        self.invulnerability_frames += 1
        if self.invulnerability_frames > 10:
            ChargeEffects.clean_damage_indicator(self.player_sprite)
