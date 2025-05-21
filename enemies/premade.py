import random
from arcade import PymunkPhysicsEngine
from parameters import *
from enemies.enemy import Enemy
from resource_manager import get_slime_sprite, get_rat_sprite, get_wizard_sprite, get_mimic_sprite

def get_random_enemies(n, d):
    e_list = []
    for i in range(n):
        r = random.randint(1, 4)
        if r == 1:
            e_list.append(Slime(d))
        elif r == 2:
            e_list.append(Rat(d))
        elif r == 3:
            e_list.append(Wizard(d))
        elif r == 5:
            e_list.append(Goblin(d))
    return e_list

def get_random_boss(d):
    t = random.randint(1, 4)
    if t == 1:
        e = Slime(d+2)
    elif t == 2:
        e = Wizard(d + 2)
    elif t == 3:
        e = Goblin(d + 2)
    else:
        e = Rat(d + 2)
    e.sprite.scale = e.sprite.scale * 3
    return e

class Slime(Enemy):
    def __init__(self, difficulty):
        d = 1 + difficulty
        super().__init__(
            health=int(5*d),
            damage=int(1*d),
            speed=10,
            attack_range=32,
            attack_cooldown=3,
            position = (random.randint(SPRITE_SIZE*4, WINDOW_WIDTH-SPRITE_SIZE*4), random.randint(SPRITE_SIZE*4, WINDOW_WIDTH-SPRITE_SIZE*4)),
            sprite_handle=get_slime_sprite
        )
        self.sprite.scale = 1

    def attack(self, delta_time, destination, engine: PymunkPhysicsEngine, projectile_control):
        super().melee_attack(delta_time, destination, engine)

    def move(self, destination, engine: PymunkPhysicsEngine, **kwargs):
        super().basic_move(destination, engine)


class Rat(Enemy):
    def __init__(self, difficulty):
        d = 1 + difficulty
        super().__init__(
            health=int(3*d),
            damage=int(1*d),
            speed=10,
            attack_range=32,
            attack_cooldown=3,
            position = (random.randint(SPRITE_SIZE*4, WINDOW_WIDTH-SPRITE_SIZE*4), random.randint(SPRITE_SIZE*4, WINDOW_WIDTH-SPRITE_SIZE*4)),
            sprite_handle=get_rat_sprite
        )
        self.sprite.scale = 1

    def attack(self, delta_time, destination, engine: PymunkPhysicsEngine, projectile_control):
        super().melee_attack(delta_time, destination, engine)

    def move(self, destination, engine: PymunkPhysicsEngine, **kwargs):
        super().basic_move(destination, engine)

class Wizard(Enemy):
    def __init__(self, difficulty):
        d = 1 + difficulty
        super().__init__(
            health=int(7*d),
            damage=int(1*d),
            speed=10,
            attack_range=32,
            attack_cooldown=2,
            position = (random.randint(SPRITE_SIZE*4, WINDOW_WIDTH-SPRITE_SIZE*4), random.randint(SPRITE_SIZE*4, WINDOW_WIDTH-SPRITE_SIZE*4)),
            sprite_handle=get_wizard_sprite
        )
        self.sprite.scale = 1

    def attack(self, delta_time, destination, engine: PymunkPhysicsEngine, projectile_control):
        super().ranged_attack(delta_time,destination, projectile_control)

    def move(self, destination, engine: PymunkPhysicsEngine, **kwargs):
        super().keep_away(destination, engine, 25)

class Mimic(Enemy):
    def __init__(self, difficulty):
        d = 1 + difficulty
        super().__init__(
            health=int(6*d),
            damage=int(2*d),
            speed=10,
            attack_range=32,
            attack_cooldown=3,
            position = (random.randint(SPRITE_SIZE*4, WINDOW_WIDTH-SPRITE_SIZE*4), random.randint(SPRITE_SIZE*4, WINDOW_WIDTH-SPRITE_SIZE*4)),
            sprite_handle=get_mimic_sprite
        )
        self.sprite.scale = 1

    def attack(self, delta_time, destination, engine: PymunkPhysicsEngine, projectile_control):
        super().melee_attack(delta_time, destination, engine)

    def move(self, destination, engine: PymunkPhysicsEngine, **kwargs):
        super().wait_until_interact(destination, engine)

    def update(self, delta_time):
        if self.sprite.properties["interact"]:
            super().update(delta_time)

class Goblin(Enemy):
    def __init__(self, difficulty):
        d = 1 + difficulty
        super().__init__(
            health=int(5*d),
            damage=int(1*d),
            speed=8,
            attack_range=32,
            attack_cooldown=3,
            position = (random.randint(SPRITE_SIZE*4, WINDOW_WIDTH-SPRITE_SIZE*4), random.randint(SPRITE_SIZE*4, WINDOW_WIDTH-SPRITE_SIZE*4)),
            sprite_handle=get_rat_sprite
        )
        self.sprite.scale = 1

    def attack(self, delta_time, destination, engine: PymunkPhysicsEngine, projectile_control):
        super().melee_attack(delta_time, destination, engine)

    def move(self, destination, engine: PymunkPhysicsEngine, **kwargs):
        super().basic_move(destination, engine)
