# damage manager singleton
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
        if stats.health > 0 and self.invulnerability_frames >= 60:
            print("damage_taken")
            stats.health -= 1  # Or use stats.take_damage(1) if you have a method
            self.invulnerability_frames = 0

    def update(self):
        self.invulnerability_frames += 1