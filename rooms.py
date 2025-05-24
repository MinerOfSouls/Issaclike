import random
from abc import abstractmethod
from os import remove

import arcade
from arcade import PymunkPhysicsEngine
from arcade.hitbox import pymunk

from collectables.room_clear_reward import SpawnRandomReward
from enemies.premade import get_random_enemies, get_random_boss, Mimic
from enemies.enemy import EnemyController
from parameters import *
from collectables.pickup_factory import PickupFactory
from characters.stats import  PlayerStatsController
from resource_manager import get_door_texture, get_wall_texture, get_floor, get_stairs

random.seed(1234)

NEXT_ROOM_POSITIONS = {
    "north":(SPRITE_SIZE * ((WINDOW_WIDTH/SPRITE_SIZE)//2) - SPRITE_SIZE//2, 2*SPRITE_SIZE),
    "south":(SPRITE_SIZE * ((WINDOW_WIDTH/SPRITE_SIZE)//2) - SPRITE_SIZE//2, WINDOW_HEIGHT - 2*SPRITE_SIZE),
    "west":(2*SPRITE_SIZE, SPRITE_SIZE * ((WINDOW_HEIGHT/SPRITE_SIZE)//2) - SPRITE_SIZE//2),
    "east":(WINDOW_WIDTH - 2*SPRITE_SIZE, SPRITE_SIZE * ((WINDOW_HEIGHT/SPRITE_SIZE)//2) - SPRITE_SIZE//2)
}

def door_side(x, y):
    if y == 0:
        return "south"
    elif y == WINDOW_HEIGHT - SPRITE_SIZE:
        return "north"
    elif x == 0:
        return "east"
    else:
        return "west"

class Room:
    #wall_sprites is a dictionary based on position with keys:
    #"north", "east", "west", "south" and values being paths to sprite pngs
    def __init__(self, doors, engine):
        self.wall_list = arcade.SpriteList()
        self.doors = arcade.SpriteList()
        self.completed = False
        self.physics_engine = engine
        self.objects = arcade.SpriteList()
        self.effects_list = arcade.SpriteList()
        self.stats = PlayerStatsController()
        self.loaded = False
        self.spawn_reward = SpawnRandomReward(self.physics_engine , self.objects, self.effects_list ,self.stats)
        self.reward_spawned = False


        def draw_wall(x, y):
            wall = arcade.Sprite(get_wall_texture(x, y), scale=SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            self.wall_list.append(wall)

        def draw_door(x, y):
            if door_side(x, y) not in doors:
                draw_wall(x, y)
                return
            door = arcade.Sprite(
                get_door_texture(x, y, self.completed),
                scale=SPRITE_SCALING
            )
            door.left = x
            door.bottom = y
            self.doors.append(door)

        #Generating top and bottom walls
        for y in (0, WINDOW_HEIGHT - SPRITE_SIZE):
            for x in range(0, WINDOW_WIDTH, SPRITE_SIZE):
                if x != SPRITE_SIZE * ((WINDOW_WIDTH/SPRITE_SIZE)//2) and x != SPRITE_SIZE * ((WINDOW_WIDTH/SPRITE_SIZE)//2 - 1):
                    draw_wall(x, y)
                else:
                    draw_door(x, y)


        #Generating the left right walls
        for x in (0, WINDOW_WIDTH - SPRITE_SIZE):
            for y in range(SPRITE_SIZE, WINDOW_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
                if y != SPRITE_SIZE * ((WINDOW_HEIGHT/SPRITE_SIZE)//2) and y != SPRITE_SIZE * ((WINDOW_HEIGHT/SPRITE_SIZE)//2 - 1):
                    draw_wall(x, y)
                else:
                    draw_door(x, y)

    def draw(self):
        arcade.draw_texture_rect(
            get_floor(),
            rect=arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        self.wall_list.draw(pixelated=True)
        self.doors.draw(pixelated=True)
        self.effects_list.draw()
        self.objects.draw()

    def spawn_reward_fun(self):
        if self.completed and not self.reward_spawned:
            item =self.spawn_reward.on_room_clear()
            self.reward_spawned = True

    def complete(self):
        self.completed = True
        for door in self.doors:
            door.texture = get_door_texture(door.left, door.bottom, self.completed)
        self.spawn_reward_fun()

    def update(self, delta_time, player):
        self.effects_list.update()
        self.objects.update()

        # # da sie ujednolicić
        for effect in self.effects_list:
            if effect.should_delete:
                self.effects_list.remove(effect)
                self.physics_engine.remove_sprite(effect)


    def enter(self):
        self.loaded = True
        print("entered")
        print(self.completed)
        print(self.reward_spawned)
        for object in self.objects:
            print(object, end=" ")
        for wall in self.wall_list:
            self.physics_engine.add_sprite(wall, body_type=2, collision_type="wall")
        for door in self.doors:
            self.physics_engine.add_sprite(door, body_type=2, collision_type="door")

        for pickup in self.objects:
            pickup.on_setup()
            print("pickup setup", pickup)

    def leave(self):
        self.loaded = False
        for s in self.doors:
            self.physics_engine.remove_sprite(s)
        for s in self.wall_list:
            self.physics_engine.remove_sprite(s)

        for effect in self.effects_list:
            self.effects_list.remove(effect)
            self.physics_engine.remove_sprite(effect)

        for item_obj in self.objects:
                try:
                    item_obj.is_physics_setup = False
                    item_obj.remove_from_physics_engine()
                except KeyError:
                    pass


class EnemyRoom(Room):
    def __init__(self,doors, engine, enemies, stats):
        super().__init__(doors, engine)
        self.enemy_controller = EnemyController(enemies, self, engine, stats, self.objects)

    def update(self, delta_time, player):
        super().update(delta_time, player)
        self.enemy_controller.update(delta_time, player)

    def draw(self):
        super().draw()
        self.enemy_controller.draw()

    def enter(self):
        super().enter()
        self.enemy_controller.add_enemies_to_engine()

    def leave(self):
        super().leave()
        self.enemy_controller.remove_enemies_from_engine()

class BossRoom(EnemyRoom):
    def __init__(self, doors, engine, d, stats):
        super().__init__(doors, engine, [get_random_boss(d)], stats)
        self.stairs = arcade.SpriteList()

    def complete(self):
        super().complete()
        stairs = arcade.Sprite(get_stairs(), SPRITE_SCALING, WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        self.physics_engine.add_sprite(stairs, body_type=2, collision_type="stairs")
        self.stairs.append(stairs)

    def draw(self):
        super().draw()
        self.stairs.draw()

    def leave(self):
        super().leave()
        for s in self.stairs:
            self.physics_engine.remove_sprite(s)

    def enter(self):
        super().enter()
        for s in self.stairs:
            self.physics_engine.add_sprite(s, body_type=2, collision_type="stairs")

class TreasureRoom(Room):
    def __init__(self, doors, engine):
        super().__init__(doors, engine)

        # for object in self.objects:
        #     self.physics_engine.remove_sprite(object)
    def enter(self):
        self.complete()
        super().enter()


    def spawn_reward_fun(self):
        if self.completed and not self.reward_spawned:
            item =self.spawn_reward._spawn_chest()
            item.on_setup()

            self.reward_spawned = True

class Map:
    def __init__(self, n, physics_engine, stats, special_ability):
        self.physics_engine = physics_engine
        self.special_ability = special_ability
        self.mini_map = {}
        self.rooms = {}

        # Room generation
        room_coordinates = [(0, 0)]
        i = 1
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        while i < n:
            r = random.sample(room_coordinates, 1)[0]
            d = random.sample(directions, 1)[0]
            new = (r[0] + d[0], r[1] + d[1])
            if new in room_coordinates:
                continue
            else:
                room_coordinates.append(new)
                i += 1

        self.connections = {coords:{} for coords in room_coordinates}
        #Connecting rooms
        for r in room_coordinates:
            neighbours = [(r[0] + d[0], r[1] + d[1]) for d in directions]
            for n_i in range(4):
                nb = neighbours[n_i]
                key = ""
                match n_i:
                    case 0:
                        key = "north"
                    case 1:
                        key = "south"
                    case 2:
                        key = "west"
                    case 3:
                        key = "east"
                if nb in room_coordinates:
                    self.connections[r][key] = nb
        direction_keys = ["north", "south", "east", "west"]
        #Assing room types
        # 0 - start, 1 - end, 2 - enemy room, 3 - treasure room
        room_types = {(0,0):0, room_coordinates[-1]:1}
        for i in range(1, n-1):
            r = random.random()
            if r < 0.2:
                room_types[room_coordinates[i]] = 3
            else:
                room_types[room_coordinates[i]] = 2
        #Generating Room objects
        for c in room_coordinates:
            room_doors = {k for k in self.connections[c].keys()}
            if room_types[c] == 0:
                self.rooms[c] = Room(room_doors, self.physics_engine)
            elif room_types[c] == 1:
                self.rooms[c] = BossRoom(room_doors, self.physics_engine, 0, stats)
            elif room_types[c] == 2:
                self.rooms[c] = EnemyRoom(room_doors, self.physics_engine, get_random_enemies(3, 0), stats)
            elif room_types[c] == 3:
                r = random.random()
                if r < 0.8:
                    self.rooms[c] = TreasureRoom(room_doors, self.physics_engine)
                else:
                    self.rooms[c] = EnemyRoom(room_doors, self.physics_engine, [Mimic(0)], stats)

        self.mini_map = room_types
        self.current_room = (0, 0)
        self.rooms[(0, 0)].complete()

    def on_setup(self):

        #  door transition handler
        def door_interact_handler(player_sprite, door_sprite, *args):
            if self.change_room(player_sprite, door_sprite, self.physics_engine):
                self.special_ability.delete_effect_on_room_transition()
                return True
            else:
                return False

        self.physics_engine.add_collision_handler("player", "door", post_handler=door_interact_handler)

        self.rooms[self.current_room].enter()

    def get_current_walls(self):
        return self.rooms[self.current_room].wall_list

    def get_current_doors(self):
        return self.rooms[self.current_room].doors

    def check_room_move(self, door):
        if int(door.left) == 0:
            return "east"
        elif int(door.left) ==  WINDOW_WIDTH - SPRITE_SIZE:
            return "west"
        elif int(door.bottom) == 0:
            return "south"
        elif int(door.bottom) == WINDOW_HEIGHT - SPRITE_SIZE:
            return "north"
        else:
            return False

    def change_room(self, player_sprite: arcade.Sprite, door_sprite, engine: PymunkPhysicsEngine):
        check = self.check_room_move(door_sprite)
        if check is not False and self.rooms[self.current_room].completed:
            if check in self.connections[self.current_room].keys():
                self.rooms[self.current_room].leave()
                pos = (NEXT_ROOM_POSITIONS[check][0], NEXT_ROOM_POSITIONS[check][1])
                engine.set_position(player_sprite, pos)
                self.current_room = self.connections[self.current_room][check]
                self.rooms[self.current_room].enter()
                print(self.current_room)
                return True
            else:
                # TODO: add exception here maybe (player exited the room in an illegal direction)
                pass
        else:
            return False

    def draw(self):
        self.rooms[self.current_room].draw()

    def update(self, delta_time, player):
        self.rooms[self.current_room].update(delta_time, player)

    def get_object_list(self):
        return self.rooms[self.current_room].objects

    def get_effect_list(self):
        return self.rooms[self.current_room].objects

    def is_loaded(self):
        return self.rooms[self.current_room].loaded

    def get_enemy_controller(self):
        if type(self.rooms[self.current_room]) == EnemyRoom:
            return self.rooms[self.current_room].enemy_controller
        else:
            return False