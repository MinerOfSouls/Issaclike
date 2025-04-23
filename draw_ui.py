from characters.stats import PlayerStatsController
import arcade
import arcade.gui
from animations.hearth import Hearth
from parameters import *
from pyglet.graphics import Batch
arcade.resources.load_kenney_fonts()

DEFAULT_LINE_HEIGHT = 50  # Line height to use in pixels
DEFAULT_FONT_SIZE = 15  # Default font size in points

#todo scaling everything is fixed position and does not scale properly
TEXTURES = {
"hearth":"resources/images/heart_animated_1.png",
"coin":"resources/images/coin.png",
"key":"resources/images/key-white.png",
}

class DrawUI:
    def __init__(self, stats:PlayerStatsController):
        super().__init__()

        self.stats = stats
        self.sprite_list = arcade.SpriteList()

        self.batch = Batch()

        hearth_sheet = arcade.load_spritesheet(TEXTURES["hearth"])
        coin_sheet = arcade.load_spritesheet(TEXTURES["coin"])
        key_sheet = arcade.load_spritesheet(TEXTURES["key"])

        hearth_texture = hearth_sheet.get_texture_grid(size=(17,17),columns=5,count=5)
        coin_texture = coin_sheet.get_texture_grid(size=(80,80),columns=8,count=8)
        key_texture = key_sheet.get_texture_grid(size=(32,32),columns=12,count=12)

        for i in range(stats.health):
            self.hearth = Hearth(hearth_texture)
            self.hearth.position = 25+i*25 , WINDOW_HEIGHT-25
            self.sprite_list.append(self.hearth)

        self.coin_UI = arcade.Sprite(coin_texture[0] , scale=0.25)
        self.coin_UI.position = 25, WINDOW_HEIGHT- 50
        self.sprite_list.append(self.coin_UI)

        self.key_UI = arcade.Sprite(key_texture[0] , scale=0.75)
        self.key_UI.position  = 25, WINDOW_HEIGHT- 75
        self.sprite_list.append(self.key_UI)

    def on_draw(self) -> None:
        self.sprite_list.draw()
        self.batch.draw()
    def on_update(self):
        start_x = 40
        start_y = WINDOW_HEIGHT- 60
        self.coin_count = arcade.Text(
            self.stats.get_coin_number(),
            start_x,
            start_y,
            arcade.color.BLACK,
            DEFAULT_FONT_SIZE,
            font_name="Kenney Blocks",
            batch=self.batch,
        )
        start_y = WINDOW_HEIGHT - 85
        self.key_count = arcade.Text(
            self.stats.get_key_number(),
            start_x,
            start_y,
            arcade.color.BLACK,
            DEFAULT_FONT_SIZE,
            font_name="Kenney Blocks",
            batch=self.batch,
        )
        start_y = WINDOW_HEIGHT - 110
        self.bomb_count = arcade.Text(
            self.stats.get_bomb_number(),
            start_x,
            start_y,
            arcade.color.BLACK,
            DEFAULT_FONT_SIZE,
            font_name="Kenney Blocks",
            batch=self.batch,
        )

        self.sprite_list.update()
        self.batch.draw()

