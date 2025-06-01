class Stats:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, speed=10, damage=1, projectile_speed=150, projectile_cooldown=25,
                 luck=0, projectile_range=800, health=6, coins=0, keys=1, bombs=0):
        if getattr(self, '__initialized', False):
            return

        self.speed = speed
        self.damage = damage
        self.projectile_speed = projectile_speed
        self.projectile_cooldown = projectile_cooldown
        self.luck = luck
        self.range = projectile_range
        self.health = health
        self.coins = coins
        self.keys = keys
        self.bombs = bombs
        self.invincible = False
        self.ability_active = False

        self.__initialized = True

    def get_coin_number(self):
        return f"{self.coins:02d}"

    def get_key_number(self):
        return f"{self.keys:02d}"

    def get_bomb_number(self):
        return f"{self.bombs:02d}"

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
