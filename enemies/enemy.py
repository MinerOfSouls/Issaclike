import math
import arcade
import random
from typing import List
from arcade import PymunkPhysicsEngine
from parameters import *


class Enemy:
    def __init__(self, health, damage, speed, position, armour, texture):
        self.sprite = arcade.Sprite(texture, scale = SPRITE_SCALING, center_x=position[0], center_y=position[1])
        self.health = health
        self.damage = damage
        self.speed = speed
        self.position = position
        #Maybe a feature
        self.armour = armour

        self.sprite.properties["health"] = self.health
        self.sprite.properties["damage"] = self.damage

    def create_path(self, destination, blockers):
        return arcade.astar_calculate_path(
            self.position,
            destination,
            arcade.AStarBarrierList(
                self.sprite,
                blockers,
                SPRITE_SIZE,
                0, WINDOW_WIDTH, 0, WINDOW_HEIGHT
            ),
            True
        )

    def add_to_engine(self, engine: PymunkPhysicsEngine):
        engine.add_sprite(
            self.sprite,
            moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
            body_type=0,
            max_velocity=self.speed,
            collision_type="enemy"
        )

    def remove_from_engine(self, engine: PymunkPhysicsEngine):
        engine.remove_sprite(self.sprite)

    def move(self, destination, engine: PymunkPhysicsEngine):
        x_goal = destination[0]
        y_goal = destination[1]
        x_delta = x_goal - self.position[0]
        y_delta = y_goal - self.position[1]
        angle = math.atan2(y_delta, x_delta)
        dist = math.dist(self.position, destination)
        speed = min(self.speed, dist)
        change_x = math.cos(angle) * speed
        change_y = math.sin(angle) * speed
        engine.apply_impulse(self.sprite, (change_x, change_y))

class EnemyController:
    def __init__(self, enemies: List[Enemy], room, engine: PymunkPhysicsEngine):
        self.enemies = enemies
        self.enemy_sprite_list = arcade.SpriteList()
        for e in self.enemies:
            self.enemy_sprite_list.append(e.sprite)
        self.physics_engine = engine
        self.room = room

        #TODO
        def player_collision_handler(*args):
            return False

        def projectile_collision_handler(
                                         enemy_sprite: arcade.Sprite,
                                         projectile_sprite: arcade.Sprite, *args):
            projectile_sprite.remove_from_sprite_lists()

            # TODO add specific projectile damage
            enemy_sprite.properties["health"] -= 1
            if enemy_sprite.properties["health"] <= 0:
                enemy_sprite.remove_from_sprite_lists()
            return False

        self.physics_engine.add_collision_handler("enemy", "projectile", post_handler=projectile_collision_handler)
        self.physics_engine.add_collision_handler("enemy", "player", begin_handler=player_collision_handler)

    def draw(self):
        self.enemy_sprite_list.draw()

    #temprarly removed room completion logic
    def update(self, player: arcade.Sprite):
        if len(self.enemy_sprite_list) == 0:
            self.room.completed = True
            self.enemies.clear()
            return
        location = (player.center_x, player.center_y)
        garbage_collect = []
        for e in self.enemies:
            if e.sprite not in self.enemy_sprite_list:
                garbage_collect.append(e)
                continue
            e.move(location, self.physics_engine)
            if e.sprite.center_x < 0 or e.sprite.center_x > WINDOW_WIDTH:
                e.sprite.remove_from_sprite_lists()
                garbage_collect.append(e)
            elif e.sprite.center_y < 0 or e.sprite.center_y > WINDOW_HEIGHT:
                e.sprite.remove_from_sprite_lists()
                garbage_collect.append(e)
        for e in garbage_collect:
            self.enemies.remove(e)

    def add_enemies_to_engine(self):
        for e in self.enemies:
            e.add_to_engine(self.physics_engine)

    def remove_enemies_from_engine(self):
        print(self.enemies, len(self.enemy_sprite_list))
        for e in self.enemies:
            e.remove_from_engine(self.physics_engine)

def create_random_enemies(n):
    e_list = []
    for i in range(n):
        e_list.append(Enemy(
            random.randint(0, 10),
            random.randint(0, 10),
            10,
            (random.randint(SPRITE_SIZE*4, WINDOW_WIDTH-SPRITE_SIZE*4), random.randint(SPRITE_SIZE*4, WINDOW_WIDTH-SPRITE_SIZE*4)),
            0,
            "resources/images/enemy_placeholder.png"
        ))
    return e_list
