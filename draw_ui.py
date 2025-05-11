from characters.stats import PlayerStatsController
import arcade
import arcade.gui

from collectables.animation import Animation
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

# todo stupid and unefficient implementaion but it works change it later

hearth_url = 'resources/images/heart_animated_1.png'
hearth_details = {
    "width": 17,
    "height": 17,
    "columns": 5,
    "count": 5,
    "speed": 0.3,
    "scale": 1.5,
    "looping": True
}

class DrawUI:
    def __init__(self, stats:PlayerStatsController):
        super().__init__()

        self.stats = stats
        self.sprite_list = arcade.SpriteList()
        self.health_list = arcade.SpriteList()
        self.previous_health = 0

        self.batch = Batch()

        coin_sheet = arcade.load_spritesheet(TEXTURES["coin"])
        key_sheet = arcade.load_spritesheet(TEXTURES["key"])


        coin_texture = coin_sheet.get_texture_grid(size=(80,80),columns=8,count=8)
        key_texture = key_sheet.get_texture_grid(size=(32,32),columns=12,count=12)

        self.update_health()

        self.coin_UI = arcade.Sprite(coin_texture[0] , scale=0.25)
        self.coin_UI.position = 25, WINDOW_HEIGHT- 50
        self.sprite_list.append(self.coin_UI)

        self.key_UI = arcade.Sprite(key_texture[0] , scale=0.75)
        self.key_UI.position  = 25, WINDOW_HEIGHT- 75
        self.sprite_list.append(self.key_UI)

    def update_health(self):
        if self.previous_health != self.stats.health:
            # Clear existing health sprites from both lists
            for sprite in self.health_list:
                if sprite in self.sprite_list:
                    self.sprite_list.remove(sprite)
            self.health_list.clear()

            # Add new health sprites if health > 0
            if self.stats.health > 0:
                for i in range(self.stats.health):
                    heart = Animation(hearth_url, hearth_details)
                    heart.position = 25 + i * 25, WINDOW_HEIGHT - 25
                    self.health_list.append(heart)
                    self.sprite_list.append(heart)

            self.previous_health = self.stats.health

    def on_draw(self) -> None:
        self.sprite_list.draw()
        self.batch.draw()

    def on_update(self):
        self.update_health()
        start_x = 40
        start_y = WINDOW_HEIGHT- 60
        self.coin_count = arcade.Text(
            self.stats.get_coin_number(),
            start_x,
            start_y,
            arcade.color.WHITE,
            DEFAULT_FONT_SIZE,
            font_name="Kenney Blocks",
            batch=self.batch,
        )
        start_y = WINDOW_HEIGHT - 85
        self.key_count = arcade.Text(
            self.stats.get_key_number(),
            start_x,
            start_y,
            arcade.color.WHITE,
            DEFAULT_FONT_SIZE,
            font_name="Kenney Blocks",
            batch=self.batch,
        )
        start_y = WINDOW_HEIGHT - 110
        self.bomb_count = arcade.Text(
            self.stats.get_bomb_number(),
            start_x,
            start_y,
            arcade.color.WHITE,
            DEFAULT_FONT_SIZE,
            font_name="Kenney Blocks",
            batch=self.batch,
        )

        self.sprite_list.update()
        self.batch.draw()

