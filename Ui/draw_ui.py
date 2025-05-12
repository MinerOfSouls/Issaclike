from Ui.mini_map import MiniMap
from characters.stats import PlayerStatsController
import arcade
import arcade.gui

from collectables.animation import Animation
from parameters import *
from pyglet.graphics import Batch
from resource_manager import get_object
arcade.resources.load_kenney_fonts()

DEFAULT_LINE_HEIGHT = 50  # Line height to use in pixels
DEFAULT_FONT_SIZE = 15  # Default font size in points


class DrawUI:
    def __init__(self, stats:PlayerStatsController , map):
        super().__init__()

        self.stats = stats
        self.sprite_list = arcade.SpriteList()
        self.health_list = arcade.SpriteList()
        self.previous_health = 0
        self.mini_map = MiniMap(map)

        self.batch = Batch()
        coin_texture = get_object("coin")[0]
        key_texture =get_object("key")[0]

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
                    sprite = get_object("heart")
                    heart = Animation(sprite[0], sprite[1])
                    heart.position = 25 + i * 25, WINDOW_HEIGHT - 25
                    self.health_list.append(heart)
                    self.sprite_list.append(heart)

            self.previous_health = self.stats.health

    def on_draw(self) -> None:
        self.sprite_list.draw()
        self.mini_map.draw()
        self.batch.draw()


    def on_update(self):
        self.mini_map.update()
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

