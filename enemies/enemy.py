import math
import arcade
import random
from typing import List
from arcade import PymunkPhysicsEngine

from effects.charge_effect import ChargeEffects
from effects.item_effects import ItemEffects
from parameters import *

class Enemy:
    def __init__(self, health, damage, speed, position, attack_cooldown, attack_range, sprite_handle):
        self.sprite = sprite_handle()
        self.health = health
        self.max_health = health
        self.damage = damage
        self.speed = speed
        self.position = position
        self.attack_cooldown = attack_cooldown
        self.timer = attack_cooldown
        self.attack_range = attack_range

        self.sprite.scale = 1
        self.sprite.center_x = position[0]
        self.sprite.center_y = position[1]

        self.sprite.properties["health"] = self.health
        self.sprite.properties["damage"] = self.damage
        self.sprite.properties["interact"] = False

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

    def move(self, destination, engine: PymunkPhysicsEngine, **kwargs):
        self.basic_move(destination, engine)
        pass

    def attack(self, delta_time, destination, engine: PymunkPhysicsEngine, projectile_control):
        pass

    def update(self):
        self.position = (self.sprite.center_x, self.sprite.center_y)
        self.health = self.sprite.properties["health"]

    def __move_calc(self, destination):
        x_goal = destination[0]
        y_goal = destination[1]
        x_delta = x_goal - self.position[0]
        y_delta = y_goal - self.position[1]
        angle = math.atan2(y_delta, x_delta)
        dist = math.dist(self.position, destination)
        speed = min(self.speed, dist)
        change_x = math.cos(angle) * speed
        change_y = math.sin(angle) * speed
        return change_x, change_y

    # Movement algorithm types
    def basic_move(self, destination, engine: PymunkPhysicsEngine):
        change_x, change_y = self.__move_calc(destination)
        engine.apply_impulse(self.sprite, (change_x, change_y))

    def keep_away(self, destination, engine: PymunkPhysicsEngine, keep_away_distance):
        change_x, change_y = self.__move_calc(destination)
        dist = math.dist(self.position, destination)
        if dist < keep_away_distance:
            engine.apply_impulse(self.sprite, (-change_x, -change_y))
        else:
            engine.apply_impulse(self.sprite, (change_x, change_y))

    def move_along_path(self, engine: PymunkPhysicsEngine, path, current_id):
        if current_id >= len(path):
            current_id = 0
        destination = path[current_id]
        change_x, change_y = self.__move_calc(destination)
        engine.apply_impulse(self.sprite, (change_x, change_y))

    def wait_until_interact(self, destination, engine: PymunkPhysicsEngine):
        if self.sprite.properties["interact"]:
            self.basic_move(destination, engine)

    def melee_attack(self, delta_time, destination, engine: PymunkPhysicsEngine):
        if self.timer > 0:
            self.timer -= delta_time
            return
        dist = math.dist(self.position, destination)
        if dist < self.attack_range:
            attack_sprite = arcade.Sprite(None, center_x=destination[0], center_y=destination[1])
            attack_sprite.size = (SPRITE_SIZE, SPRITE_SIZE)
            attack_sprite.properties["tmp"] = True
            attack_sprite.properties["damage"] = self.damage
            self.melee_attack_sprite = attack_sprite
            engine.add_sprite(
                attack_sprite,
                body_type=2,
                collision_type="enemy"
            )
            self.timer = self.attack_cooldown

    def ranged_attack(self, delta_time, destination, projectile_control):
        if self.timer > 0:
            self.timer -= delta_time
            return
        projectile_control.spawn_projectile(self, destination)
        self.timer = self.attack_cooldown


class EnemyController:
    def __init__(self, enemies: List[Enemy], room, engine: PymunkPhysicsEngine, stats,effect_list):
        self.enemies = enemies
        self.enemy_sprite_list = arcade.SpriteList()
        for e in self.enemies:
            self.enemy_sprite_list.append(e.sprite)
        self.physics_engine = engine
        self.room = room
        self.stats = stats
        self.projectiles = EnemyProjectileController(engine, stats, 10)
        self.effect_list = effect_list

        def player_collision_handler(enemy_sprite: arcade.Sprite, player_sprite: arcade.Sprite, *args):
            enemy_sprite.properties["interact"] = True
            if not player_sprite.properties["invincible"]:
                self.stats.health = max(1, self.stats.health - enemy_sprite.properties["damage"])
                player_sprite.properties["invincible"] = True
                player_sprite.properties["inv_timer"] = 1.0
            if "tmp" in enemy_sprite.properties.keys():
                print("hit")
                enemy_sprite.remove_from_sprite_lists()
            return False

        def projectile_collision_handler(
                                         enemy_sprite: arcade.Sprite,
                                         projectile_sprite: arcade.Sprite, *args):
            projectile_sprite.remove_from_sprite_lists()

            enemy_sprite.properties["health"] -= self.stats.damage
            if enemy_sprite.properties["health"] <= 0:
                enemy_sprite.remove_from_sprite_lists()
            return False

        def enemy_hit_handle(enemy_sprite: arcade.Sprite, *args):
            enemy_sprite.properties["health"] -= self.stats.damage
            if enemy_sprite.properties["health"] <= 0:
                enemy_sprite.remove_from_sprite_lists()
            return False

        self.physics_engine.add_collision_handler("enemy", "projectile", post_handler=projectile_collision_handler)
        self.physics_engine.add_collision_handler("enemy", "player", begin_handler=player_collision_handler)
        self.physics_engine.add_collision_handler("enemy", "sword", post_handler=enemy_hit_handle)
        self.physics_engine.add_collision_handler("enemy", "boomerang", post_handler=enemy_hit_handle)

    def draw(self):
        self.projectiles.draw()
        self.enemy_sprite_list.draw()

    #temprarly removed room completion logic
    def update(self, delta_time, player: arcade.Sprite):

        self.projectiles.update()

        if player.properties["invincible"]:
            player.properties["inv_timer"] -= delta_time
            if player.properties["inv_timer"] <= 0:
                player.properties["inv_timer"] = 0
                player.properties["invincible"] = False

        if len(self.enemy_sprite_list) == 0 and not self.room.completed:
            self.room.complete()
            self.enemies.clear()
            return
        location = (player.center_x, player.center_y)
        garbage_collect = []
        for e in self.enemies:
            if e.sprite not in self.enemy_sprite_list:
                garbage_collect.append(e)
                continue
            if e.sprite.center_x < 0 or e.sprite.center_x > WINDOW_WIDTH:
                e.sprite.remove_from_sprite_lists()
                garbage_collect.append(e)
                continue
            elif e.sprite.center_y < 0 or e.sprite.center_y > WINDOW_HEIGHT:
                e.sprite.remove_from_sprite_lists()
                garbage_collect.append(e)
                continue

            e.update()
            e.move(location, self.physics_engine)
            e.sprite.update(delta_time)
            e.attack(delta_time, location, self.physics_engine, self.projectiles)

        for e in garbage_collect:
            self.enemies.remove(e)

    def add_enemies_to_engine(self):
        for e in self.enemies:
            e.add_to_engine(self.physics_engine)

    def remove_enemies_from_engine(self):
        # print(self.enemies, len(self.enemy_sprite_list))
        for e in self.enemies:
            e.remove_from_engine(self.physics_engine)

class EnemyProjectileController:
    def __init__(self, engine: PymunkPhysicsEngine, stats, speed):
        self.physics_engine = engine
        self.projectiles = arcade.SpriteList()
        self.projectile_speed = speed
        self.stats = stats

        def player_hit_handler(enemy_projectile_sprite: arcade.Sprite, player_sprite: arcade.Sprite, *args):
            if not player_sprite.properties["invincible"]:
                self.stats.health = min(1, self.stats.health - enemy_projectile_sprite.properties["damage"])
                player_sprite.properties["invincible"] = True
                player_sprite.properties["inv_timer"] = 1.0
                enemy_projectile_sprite.remove_from_sprite_lists()
            return False


        def wall_hit_handler(sprite_a, sprite_b, arbiter, space, data):
            """ Called for bullet/rock collision """
            bullet_shape = arbiter.shapes[0]
            bullet_sprite = self.physics_engine.get_sprite_for_shape(bullet_shape)
            bullet_sprite.remove_from_sprite_lists()
            return False

        self.physics_engine.add_collision_handler(
            "enemy_projectile",
            "wall",
            post_handler=wall_hit_handler
        )

        self.physics_engine.add_collision_handler(
            "enemy_projectile",
            "door",
            post_handler=wall_hit_handler
        )

        self.physics_engine.add_collision_handler(
            "enemy_projectile",
            "player",
            post_handler=player_hit_handler
        )

    def update(self):
        for projectile in self.projectiles:
            projectile_body = self.physics_engine.get_physics_object(projectile).body
            vel_x, vel_y = projectile_body.velocity
            vel_magnitude = math.sqrt(vel_x ** 2 + vel_y ** 2)

            # If velocity is too low, remove the projectile
            min_velocity = 30.0  # Adjust this threshold as needed
            if vel_magnitude < min_velocity:
                projectile.remove_from_sprite_lists()
        self.projectiles.update()

    def draw(self):
        self.projectiles.draw()

    def spawn_projectile(self, enemy: Enemy, target):
        x_goal = target[0]
        y_goal = target[1]
        x_delta = x_goal - enemy.position[0]
        y_delta = y_goal - enemy.position[1]
        angle = math.atan2(y_delta, x_delta)
        change_x = math.cos(angle) * self.projectile_speed*5
        change_y = math.sin(angle) * self.projectile_speed*5
        projectile = arcade.SpriteSolidColor(width=10, height=10, color=arcade.color.BLUE)
        projectile.center_x = enemy.position[0]
        projectile.center_y = enemy.position[1]

        projectile.properties["damage"] = enemy.damage

        self.physics_engine.add_sprite(
            projectile,
            mass=0.1,
            damping=0.01,
            friction=0.3,
            body_type=PymunkPhysicsEngine.DYNAMIC,
            collision_type="enemy_projectile",
            elasticity=0.9
        )

        body = self.physics_engine.get_physics_object(enemy.sprite).body
        vel_x, vel_y = body.velocity

        momentum_factor = 0.2
        change_x += vel_x * momentum_factor
        change_y += vel_y * momentum_factor

        self.physics_engine.apply_impulse(projectile, (change_x, change_y))
        self.projectiles.append(projectile)
