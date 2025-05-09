from parameters import *
import arcade
import os
from animations.animeted import AnimatedMovingSprite

doors = {filename.split(".")[0]:arcade.load_texture(os.path.join("resources/images/door_textures", filename))
         for filename in os.listdir("resources/images/door_textures")}

walls = {filename.split(".")[0]:arcade.load_texture(os.path.join("resources/images/wall_textures", filename))
         for filename in os.listdir("resources/images/wall_textures")}

floor = arcade.load_texture("resources/images/floor.png")

enemy_sheets = {filename.split(".")[0]:arcade.load_spritesheet(os.path.join("resources/images/enemies", filename))
                    for filename in os.listdir("resources/images/enemies")}

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

def enemy_facing(angle):
    if 0 <= angle < 180:
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
