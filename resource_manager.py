from parameters import *
import arcade
import os
from animations.animated import AnimatedMovingSprite
from collectables.animation import Animation

doors = {filename.split(".")[0]:arcade.load_texture(os.path.join("resources/images/door_textures", filename))
         for filename in os.listdir("resources/images/door_textures")}

walls = {filename.split(".")[0]:arcade.load_texture(os.path.join("resources/images/wall_textures", filename))
         for filename in os.listdir("resources/images/wall_textures")}

floor = arcade.load_texture("resources/images/floor.png")

enemy_sheets = {filename.split(".")[0]:arcade.load_spritesheet(os.path.join("resources/images/enemies", filename))
                    for filename in os.listdir("resources/images/enemies")}

player_sheets = {filename.split(".")[0]:arcade.load_spritesheet(os.path.join("resources/images/characters", filename))
                    for filename in os.listdir("resources/images/characters")}

object_sheets = {filename.split(".")[0]:arcade.load_spritesheet(os.path.join("resources/images/objects", filename))
                    for filename in os.listdir("resources/images/objects")}

object_textures = {}
object_textures["chest"] = object_sheets["chest-ss"].get_texture_grid((32, 32), 4, 4)
object_textures["coin"] = object_sheets["coin"].get_texture_grid((80, 80), 8, 8)
object_textures["leaf"] = object_sheets["ELR_FallLeaf"].get_texture_grid((16, 16), 5, 5)
object_textures["explosion"] = object_sheets["explosion"].get_texture_grid((64, 64), 30, 30)
object_textures["bomb"] = object_sheets["granade"].get_texture_grid((13, 16), 1, 1)
object_textures["health_potion"] = object_sheets["health_potion"].get_texture_grid((16, 18), 3, 3)
object_textures["heart"] = object_sheets["heart_animated_1"].get_texture_grid((17, 17), 5, 5)
object_textures["key"] = object_sheets["key-white"].get_texture_grid((32, 32), 12, 12)
object_textures["skull"] = object_sheets["skull"].get_texture_grid((16, 16), 1, 1)
object_textures["boomerang"] = object_sheets["sword"].get_texture_grid((32, 32), 11, 11)
object_textures["sword"] = object_sheets["swords1"].get_texture_grid((46, 46), 1, 1)

object_params = {
    "key":{"speed": 0.3, "scale": 0.75, "looping":True, "collectable":True, "item_type": "pick_key"},
    "coin":{"speed": 0.3, "scale": 0.25, "looping":True, "collectable":True, "item_type": "pick_coin"},
    "chest":{"speed": 0.3, "scale": 2, "looping":False},
    "health_potion":{"speed": 0.3, "scale": 1, "looping":True, "collectable":True, "item_type": "pick_health_potion"},
    "bomb":{"speed": 0.05, "scale": 2, "looping":False, "collectable":True, "item_type": "pick_bomb"},
    "skull":{"speed": 0.3, "scale": 2, "looping":False, "collectable":False, "item_type": "spawn_indicator"},
    "leaf":{"speed": 0.3, "scale": 2, "looping":True, "collectable":False, "item_type": "leaf"},
    "explosion":{"speed": 0.05, "scale": 3, "looping":False, "collectable":False, "item_type": "explosion"},
    "heart":{"speed": 0.3, "scale": 2, "looping":True, },
    "boomerang": {"speed": 0.3, "scale": 1.5, "looping": True, "collectable": False, "item_type": "boomerang"}
}

enemy_textures = {}
enemy_textures["slime_idle"] = enemy_sheets["slime_idle"].get_texture_grid((64, 64), 4, 4)
enemy_textures["slime_move_west"] = enemy_sheets["slime_move"].get_texture_grid((64, 64), 4, 4)
enemy_textures["slime_move_east"] = [t.flip_left_right() for t in enemy_textures["slime_move_west"]]

enemy_textures["rat_idle"] = enemy_sheets["rat_idle"].get_texture_grid((128, 128), 4, 4)
enemy_textures["rat_move_west"] = enemy_sheets["rat_move"].get_texture_grid((128, 128), 6, 6)
enemy_textures["rat_move_east"] = [t.flip_left_right() for t in enemy_textures["rat_move_west"]]

enemy_textures["wizard_idle"] = enemy_sheets["wizard_idle"].get_texture_grid((129, 128), 8, 8)
enemy_textures["wizard_move_west"] = enemy_sheets["wizard_move"].get_texture_grid((128, 128), 8, 8)
enemy_textures["wizard_move_east"] = [t.flip_left_right() for t in enemy_textures["wizard_move_west"]]

def get_door_texture(x, y, completed):
    door = ""
    if y == 0:
        door += "south"
    elif y == WINDOW_HEIGHT - SPRITE_SIZE:
        door += "north"
    elif x == 0:
        door += "east"
    else:
        door += "west"
    if completed:
        door += "_open"
    if x == SPRITE_SIZE * ((WINDOW_WIDTH/SPRITE_SIZE)//2):
        door += "2"
    elif  x == SPRITE_SIZE * ((WINDOW_WIDTH/SPRITE_SIZE)//2 - 1):
        door += "1"
    elif y == SPRITE_SIZE * ((WINDOW_HEIGHT/SPRITE_SIZE)//2):
        door += "2"
    elif y == SPRITE_SIZE * ((WINDOW_HEIGHT/SPRITE_SIZE)//2 - 1):
        door += "1"
    return doors[door]

def get_wall_texture(x, y):
    if x == 0 and y == 0:
        return walls["south_east"]
    elif x == 0 and y == WINDOW_HEIGHT - SPRITE_SIZE:
        return walls["north_west"]
    elif x == WINDOW_WIDTH - SPRITE_SIZE and y == 0:
        return walls["south_west"]
    elif x == WINDOW_WIDTH - SPRITE_SIZE and y == WINDOW_HEIGHT - SPRITE_SIZE:
        return walls["north_east"]
    elif y == 0:
        return walls["south"]
    elif y == WINDOW_HEIGHT - SPRITE_SIZE:
        return walls["north"]
    elif x == 0:
        return walls["west"]
    else:
        return walls["east"]

def get_floor():
    return floor

def get_object(name: str):
    if name == "sword":
        return object_textures["sword"][0]
    else:
        return object_textures[name], object_params[name]


def get_wizard_player_character():
    sprite = AnimatedMovingSprite()
    directions = ["north", "east", "west", "south"]
    idle = player_sheets["wizard_idle"].get_texture_grid((128, 128), 1, 1)
    for d in directions:
        sprite.standing_animations[d] = idle
    sprite.standing_animation_length = 1
    sprite.moving_animations["north"] = player_sheets["wizard_up"].get_texture_grid((128, 128), 6, 6)
    sprite.moving_animations["east"] = player_sheets["wizard_left"].get_texture_grid((128, 128), 6, 6)
    sprite.moving_animations["south"] = player_sheets["wizard_down"].get_texture_grid((128, 128), 6, 6)
    sprite.moving_animations["west"] = player_sheets["wizard_right"].get_texture_grid((128, 128), 6, 6)
    sprite.moving_animation_length = 6
    return sprite

def enemy_facing(angle):
    if angle < 90 or angle >= 270:
        return "east"
    else:
        return "west"

def get_slime_sprite():
    sprite = AnimatedMovingSprite()
    sprite.standing_animations["west"] = enemy_textures["slime_idle"]
    sprite.standing_animations["east"] = enemy_textures["slime_idle"]
    sprite.moving_animations["west"] = enemy_textures["slime_move_west"]
    sprite.moving_animations["east"] = enemy_textures["slime_move_east"]
    sprite.moving_animation_length = 4
    sprite.standing_animation_length = 4
    sprite.facing_calc = enemy_facing
    return sprite

def get_rat_sprite():
    sprite = AnimatedMovingSprite()
    sprite.standing_animations["west"] = enemy_textures["rat_idle"]
    sprite.standing_animations["east"] = enemy_textures["rat_idle"]
    sprite.moving_animations["west"] = enemy_textures["rat_move_west"]
    sprite.moving_animations["east"] = enemy_textures["rat_move_east"]
    sprite.moving_animation_length = 6
    sprite.standing_animation_length = 4
    sprite.facing_calc = enemy_facing
    return sprite

def get_wizard_sprite():
    sprite = AnimatedMovingSprite()
    sprite.standing_animations["west"] = enemy_textures["wizard_idle"]
    sprite.standing_animations["east"] = enemy_textures["wizard_idle"]
    sprite.moving_animations["west"] = enemy_textures["wizard_move_west"]
    sprite.moving_animations["east"] = enemy_textures["wizard_move_east"]
    sprite.moving_animation_length = 8
    sprite.standing_animation_length = 8
    sprite.facing_calc = enemy_facing
    return sprite
