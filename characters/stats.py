class PlayerStatsController:
    # todo naprawić gettery to nie java a python nie trzeba sie aż tak bawić
    ACCELERATION_RATE = 0.3
    FRICTION = 0.1
    def __init__(self, max_speed=2.5, damage=1, projectile_speed=4, projectile_cooldown=50, luck=0, range=400):
        self.max_speed = max_speed
        self.damage = damage
        self.projectile_speed = projectile_speed
        self.projectile_cooldown = projectile_cooldown
        self.luck = luck
        self.range = range

    def set_max_speed(self, max_speed):
        self.max_speed = max_speed

    def get_max_speed(self):
        return self.max_speed

    def get_acceleration(self):
        return self.ACCELERATION_RATE

    def get_friction(self):
        return self.FRICTION
    def get_projectile_speed(self):
        return self.projectile_speed
    def get_projectile_cooldown(self):
        return self.projectile_cooldown
    def get_projectile_range(self):
        return self.range
