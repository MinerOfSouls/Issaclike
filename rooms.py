import arcade
import random

from parameters import *
from arcade import PymunkPhysicsEngine

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
    def __init__(self, room_type, enemies, wall_sprites: dict, floor, door_sprites: dict):
        self.floor = arcade.load_texture(floor)
        self.enemies = enemies
        self.wall_list = arcade.SpriteList()
        self.doors = arcade.SpriteList()
        self.completed = False

        #Generating top and bottom walls
        for y in (0, WINDOW_HEIGHT - SPRITE_SIZE):
            for x in range(0, WINDOW_WIDTH, SPRITE_SIZE):
                if x != SPRITE_SIZE * ((WINDOW_WIDTH/SPRITE_SIZE)//2) and x != SPRITE_SIZE * ((WINDOW_WIDTH/SPRITE_SIZE)//2 - 1):
                    if y == 0:
                        wall = arcade.Sprite(
                            wall_sprites["south"],
                            scale=SPRITE_SCALING)
                    else:
                        wall = arcade.Sprite(
                            wall_sprites["north"],
                            scale=SPRITE_SCALING)
                    wall.left = x
                    wall.bottom = y
                    self.wall_list.append(wall)
                else:
                    if y == 0:
                        door = arcade.Sprite(
                            door_sprites["south"],
                            scale=SPRITE_SCALING
                        )
                    else:
                        door = arcade.Sprite(
                            door_sprites["north"],
                            scale=SPRITE_SCALING
                        )
                    door.left = x
                    door.bottom = y
                    self.doors.append(door)

        #Generating the left right walls
        for x in (0, WINDOW_WIDTH - SPRITE_SIZE):
            for y in range(SPRITE_SIZE, WINDOW_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
                if y != SPRITE_SIZE * ((WINDOW_HEIGHT/SPRITE_SIZE)//2) and y != SPRITE_SIZE * ((WINDOW_HEIGHT/SPRITE_SIZE)//2 - 1):
                    if x == 0:
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
                else:
                    if x == 0:
                        door = arcade.Sprite(
                            door_sprites["west"],
                            scale=SPRITE_SCALING
                        )
                    else:
                        door = arcade.Sprite(
                            door_sprites["east"],
                            scale=SPRITE_SCALING
                        )
                    door.left = x
                    door.bottom = y
                    self.doors.append(door)

    def add_to_physics(self, physics_engine):
        physics_engine.add_sprite_list(
            self.wall_list,
            friction=0.6,
            collision_type="wall",
            body_type=PymunkPhysicsEngine.STATIC
        )
        physics_engine.add_sprite_list(self.doors,
            friction=0,
            collision_type="door",
            body_type=PymunkPhysicsEngine.STATIC
        )

    def remove_from_physics(self, physics_engine):
        for wall in self.wall_list:
            physics_engine.remove_sprite(wall)

        for door in self.doors:
            physics_engine.remove_sprite(door)


class Map:
    def __init__(self, n,physics_engine):
        self.physics_engine = physics_engine
        self.rooms = {}
        self.current_room = (0, 0)

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
        #Generating Room objects
        for c in room_coordinates:
            room_doors = {k:DOOR_TEXTURES[k] for k in self.connections[c].keys()}
            for k in direction_keys:
                room_doors.setdefault(k, WALL_TEXTURES[k])
            self.rooms[c] = Room(None, None, WALL_TEXTURES, FLOOR_TEXTURE, room_doors)
            self.rooms[c].completed = True

    def on_setup(self):

        #  door transition handler
        def door_player_handler(sprite_a, sprite_b, arbiter, space, data):
            check = self.check_room_move(sprite_b)
            self.change_room(check,sprite_a)


        self.physics_engine.add_collision_handler(
            "player",
            "door",
            post_handler=door_player_handler,
        )

    def get_current_walls(self):
        return self.rooms[self.current_room].wall_list

    def get_current_doors(self):
        return self.rooms[self.current_room].doors

    def get_current_floor(self):
        return self.rooms[self.current_room].floor

    def check_room_move(self,door):
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

    def move_room(self, direction):
        if direction in self.connections[self.current_room].keys():
            self.current_room = self.connections[self.current_room][direction]
        else:
            #TODO: add exception here maybe (player exited the room in an illegal direction)
            pass

    def change_room(self,check, player_sprite: arcade.Sprite):
        if check is not False:
            # Remove old room from physics
            self.rooms[self.current_room].remove_from_physics(self.physics_engine)
            # Move to new room
            self.move_room(check)
            # Add new room to physics
            self.rooms[self.current_room].add_to_physics(self.physics_engine)
            # Move player to the right location
            self.physics_engine.set_position(player_sprite,(NEXT_ROOM_POSITIONS[check][0],NEXT_ROOM_POSITIONS[check][1]))

    def draw(self):
        arcade.draw_texture_rect(
            self.get_current_floor(),
            rect=arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        self.get_current_doors().draw()
        self.get_current_walls().draw()