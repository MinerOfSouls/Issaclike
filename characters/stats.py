class PlayerStatsController:
    def __init__(self, speed=10, damage=1, projectile_speed=100, projectile_cooldown=25, luck=0, range=400, health=6, coins =5, keys=1, bombs=1):
        self.speed = speed
        self.damage = damage
        self.projectile_speed = projectile_speed
        self.projectile_cooldown = projectile_cooldown
        self.luck = luck
        self.range = range
        self.health = health
        self.coins = coins
        self.keys = keys
        self.bombs = bombs
        self.invincible = False
        self.ability_active = False

    def get_coin_number(self):
        return f"{self.coins:02d}"
    def get_key_number(self):
        return f"{self.keys:02d}"
    def get_bomb_number(self):
        return f"{self.bombs:02d}"