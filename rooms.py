import random
from abc import abstractmethod

import arcade
from arcade import PymunkPhysicsEngine

from enemies.enemy import EnemyController, create_random_enemies
from parameters import *

random.seed(1234)

WALL_TEXTURES = {
    "north":"resources/images/wall_placeholder.png",
    "south":"resources/images/wall_placeholder.png",
    "east":"resources/images/wall_placeholder.png",
    "west":"resources/images/wall_placeholder.png"
}

DOOR_TEXTURES = {
    "north":"resources/images/door_placeholder.png",
    "south":"resources/images/door_placeholder.png",
    "east":"resources/images/door_placeholder.png",
    "west":"resources/images/door_placeholder.png"
}

FLOOR_TEXTURE = "resources/images/floor_placeholder.jpg"

NEXT_ROOM_POSITIONS = {
    "north":(SPRITE_SIZE * ((WINDOW_WIDTH/SPRITE_SIZE)//2) - SPRITE_SIZE//2, 2*SPRITE_SIZE),
    "south":(SPRITE_SIZE * ((WINDOW_WIDTH/SPRITE_SIZE)//2) - SPRITE_SIZE//2, WINDOW_HEIGHT - 2*SPRITE_SIZE),
    "east":(2*SPRITE_SIZE, SPRITE_SIZE * ((WINDOW_HEIGHT/SPRITE_SIZE)//2) - SPRITE_SIZE//2),
    "west":(WINDOW_WIDTH - 2*SPRITE_SIZE, SPRITE_SIZE * ((WINDOW_HEIGHT/SPRITE_SIZE)//2) - SPRITE_SIZE//2)
}

class Room:
    #wall_sprites is a dictionary based on position with keys:
    #"north", "east", "west", "south" and values being paths to sprite pngs
    def __init__(self, wall_sprites: dict, floor, doors, door_sprites, engine):
        self.floor = arcade.load_texture(floor)
        self.wall_list = arcade.SpriteList()
        self.doors = arcade.SpriteList()
        self.completed = False
        self.physics_engine = engine

        def draw_wall(x, y):
            if y == 0:
                wall = arcade.Sprite(
                    wall_sprites["south"],
                    scale=SPRITE_SCALING)
            elif y == WINDOW_HEIGHT - SPRITE_SIZE:
                wall = arcade.Sprite(
                    wall_sprites["north"],
                    scale=SPRITE_SCALING)
            elif x == 0:
                wall = arcade.Sprite(
                    wall_sprites["west"],
                    scale=SPRITE_SCALING)
            else:
                wall = arcade.Sprite(
                    wall_sprites["east"],
                    scale=SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            self.wall_list.append(wall)

        def draw_door(x, y):
            if y == 0:
                if "south" not in doors:
                    draw_wall(x, y)
                    return
                door = arcade.Sprite(
                    door_sprites["south"],
                    scale=SPRITE_SCALING
                )
            elif y== WINDOW_HEIGHT - SPRITE_SIZE:
                if "north" not in doors:
                    draw_wall(x, y)
                    return
                door = arcade.Sprite(
                    door_sprites["north"],
                    scale=SPRITE_SCALING
                )
            elif x == 0:
                if "west" not in doors:
                    draw_wall(x, y)
                    return
                door = arcade.Sprite(
                    door_sprites["west"],
                    scale=SPRITE_SCALING
                )
            else:
                if "east" not in doors:
                    draw_wall(x, y)
                    return
                door = arcade.Sprite(
                    door_sprites["east"],
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
        self.wall_list.draw()
        self.doors.draw()
        arcade.draw_texture_rect(
            self.floor,
            rect=arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        )

    def update(self, player):
        pass


class EnemyRoom(Room):
    def __init__(self, wall_sprites: dict, floor, doors, door_sprites, engine, enemy_n):
        super().__init__(wall_sprites, floor, doors, door_sprites, engine)
        self.enemy_controller = EnemyController(create_random_enemies(enemy_n), self, engine)

    def update(self, player):
        self.enemy_controller.update(player)

    def draw(self):
        super().draw()
        self.enemy_controller.draw()


class Map:
    def __init__(self, n,physics_engine):
        self.physics_engine = physics_engine
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
                        key = "east"
                    case 3:
                        key = "west"
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
            match room_types[c]:
                case 0: self.rooms[c] = Room(WALL_TEXTURES, FLOOR_TEXTURE, room_doors, DOOR_TEXTURES, self.physics_engine)
                case 1: self.rooms[c] = Room(WALL_TEXTURES, FLOOR_TEXTURE, room_doors, DOOR_TEXTURES, self.physics_engine)
                case 2: self.rooms[c] = EnemyRoom(WALL_TEXTURES, FLOOR_TEXTURE, room_doors, DOOR_TEXTURES, self.physics_engine, 3)
                case 3: self.rooms[c] = Room(WALL_TEXTURES, FLOOR_TEXTURE, room_doors, DOOR_TEXTURES, self.physics_engine)
            self.rooms[c].completed = True

        self.current_room = (0, 0)
        

    def on_setup(self):

        #  door transition handler
        def door_interact_handler(player_sprite, *args):
            if self.change_room(player_sprite, self.physics_engine):
                return True
            else:
                return False

        self.physics_engine.add_collision_handler("player", "door", post_handler=door_interact_handler)
        self.update_engine(self.physics_engine)

    def get_current_walls(self):
        return self.rooms[self.current_room].wall_list

    def get_current_doors(self):
        return self.rooms[self.current_room].doors

    def get_current_floor(self):
        return self.rooms[self.current_room].floor

    def update_engine(self, engine: PymunkPhysicsEngine):
        for wall in self.get_current_walls():
            engine.add_sprite(wall, body_type=2, collision_type="wall")
        for door in self.get_current_doors():
            engine.add_sprite(door, body_type=2, collision_type="door")

    def check_room_move(self, player_sprite):
        intersection = arcade.check_for_collision_with_list(player_sprite, self.get_current_doors())
        if len(intersection) ==  0:
            return False
        door = intersection[0]
        if int(door.left) == 0:
            return "west"
        elif int(door.left) ==  WINDOW_WIDTH - SPRITE_SIZE:
            return "east"
        elif int(door.bottom) == 0:
            return "south"
        elif int(door.bottom) == WINDOW_HEIGHT - SPRITE_SIZE:
            return "north"
        else:
            return False

    def change_room(self, player_sprite: arcade.Sprite, engine: PymunkPhysicsEngine):
        check = self.check_room_move(player_sprite)
        if check is not False:
            if check in self.connections[self.current_room].keys():
                for s in self.get_current_doors():
                    engine.remove_sprite(s)
                for s in self.get_current_walls():
                    engine.remove_sprite(s)
                pos = (NEXT_ROOM_POSITIONS[check][0], NEXT_ROOM_POSITIONS[check][1])
                engine.set_position(player_sprite, pos)
                self.current_room = self.connections[self.current_room][check]
                self.update_engine(self.physics_engine)
                print(self.current_room)
            else:
                # TODO: add exception here maybe (player exited the room in an illegal direction)
                pass
        else:
            return False

    def draw(self):
        self.rooms[self.current_room].draw()

    def update(self, player):
        self.rooms[self.current_room].update(player)