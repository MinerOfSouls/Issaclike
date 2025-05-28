#paramethers
from math import ceil
import arcade
screen_width, screen_height = arcade.get_display_size()
SPRITE_SCALING = 0.5
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)


WINDOW_WIDTH = int(SPRITE_SIZE * 14)
WINDOW_HEIGHT = int(SPRITE_SIZE * 10)
WINDOW_TITLE = "isaac"
resizable_scale = min(screen_width/WINDOW_WIDTH , screen_height/WINDOW_HEIGHT)
