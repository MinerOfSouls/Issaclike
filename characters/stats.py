class PlayerStatsController:
    def __init__(self, max_speed=10, damage=1, projectile_speed=100, projectile_cooldown=25, luck=0, range=400,health=6,coins =0,keys=1,bombs=1):
        self.max_speed = max_speed
        self.damage = damage
        self.projectile_speed = projectile_speed
        self.projectile_cooldown = projectile_cooldown
        self.luck = luck
        self.range = range
        self.health = health
        self.coins = coins
        self.keys = keys
        self.bombs = bombs

    def get_coin_number(self):
        return f"{self.coins:02d}"
    def get_key_number(self):
        return f"{self.keys:02d}"
    def get_bomb_number(self):
        return f"{self.bombs:02d}"