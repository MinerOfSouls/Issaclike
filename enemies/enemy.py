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

    def move(self, destination, blockers, engine: PymunkPhysicsEngine):
        self.position = (self.sprite.center_x, self.sprite.center_y)
        path = self.create_path(destination, blockers)
        x_goal = path[0][0]
        y_goal = path[0][1]
        x_delta = x_goal - self.position[0]
        y_delta = y_goal - self.position[0]
        angle = math.atan2(x_delta, y_delta)
        dist = math.dist(self.position, path[0])
        speed = min(self.speed, dist)
        change_x = math.cos(angle) * speed
        change_y = math.sin(angle) * speed
        engine.apply_force(self.sprite, (change_x, change_y))

class EnemyController:
    def __init__(self, enemies: List[Enemy], room, engine: PymunkPhysicsEngine):
        self.enemies = enemies
        self.enemy_sprite_list = arcade.SpriteList()
        for e in self.enemies:
            e.add_to_engine(engine)
            self.enemy_sprite_list.append(e.sprite)
        self.enemy_lookup = {e.sprite:e for e in self.enemies}
        self.blockers = arcade.SpriteList()
        self.blockers.extend(room.wall_list)
        self.blockers.extend(room.doors)
        self.physics_engine = engine
        self.room = room

        #TODO
        def player_collision_handler():
            pass

        def projectile_collision_handler(
                                         enemy_sprite: arcade.Sprite,
                                         projectile_sprite: arcade.Sprite, *args):
            projectile_sprite.remove_from_sprite_lists()
            hit_enemy = self.enemy_lookup[enemy_sprite]
            # TODO add specific projectile damage
            hit_enemy.health -= 1
            if hit_enemy.health <= 0:
                enemy_sprite.remove_from_sprite_lists()
                self.enemy_lookup.pop(enemy_sprite)
                self.enemies.remove(hit_enemy)
            return True

        self.physics_engine.add_collision_handler("enemy", "projectile", post_handler=projectile_collision_handler)

    def draw(self):
        self.enemy_sprite_list.draw()
    
    def update(self, player: arcade.Sprite):
        if self.room.completed:
            return
        if not self.room.completed and len(self.enemies) == 0:
            self.room.completed = True
            return
        location = (player.center_x, player.center_y)
        for e in self.enemies:
            e.move(location, self.blockers, self.physics_engine)

def create_random_enemies(n):
    e_list = []
    for i in range(n):
        e_list.append(Enemy(
            random.randint(0, 10),
            random.randint(0, 10),
            random.randint(0, 3),
            (random.randint(SPRITE_SIZE*2, WINDOW_WIDTH-SPRITE_SIZE*2), random.randint(SPRITE_SIZE*2, WINDOW_WIDTH-SPRITE_SIZE*2)),
            0,
            "resources/images/enemy_placeholder.png"
        ))
    return e_list
