import arcade
from game_view import GameView
from parameters import *

class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.stats = game_view.stats  # Assuming player_stats is accessible from game_view

    def on_show_view(self):
        self.window.background_color = arcade.color.ORANGE

    def on_draw(self):
        self.clear()

        # Draw pause text
        arcade.draw_text("PAUSED",
                         WINDOW_WIDTH / 2,
                         WINDOW_HEIGHT - 100,
                         arcade.color.BLACK,
                         font_size=50,
                         anchor_x="center",
                         bold=True)

        # Draw controls info
        arcade.draw_text("Press ESC to resume | ENTER to restart",
                         WINDOW_WIDTH / 2,
                         WINDOW_HEIGHT - 150,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

        # Draw stats box
        stats_left = WINDOW_WIDTH / 4
        stats_top = WINDOW_HEIGHT - 200
        stats_width = WINDOW_WIDTH / 2
        stats_height = 300


        # Draw stats title
        arcade.draw_text("PLAYER STATS",
                        stats_left + stats_width/2,
                        stats_top - 30,
                        arcade.color.BLACK,
                        font_size=24,
                        anchor_x="center",
                        bold=True)

        # Draw stats in two columns
        column1_x = stats_left + 30
        column2_x = stats_left + stats_width/2 + 30
        row_y = stats_top - 70
        row_spacing = 30

        # Column 1 - Core stats
        arcade.draw_text(f"Speed: {self.stats.speed}", column1_x, row_y, arcade.color.BLACK, 18)
        arcade.draw_text(f"Damage: {self.stats.damage}", column1_x, row_y - row_spacing, arcade.color.BLACK, 18)
        arcade.draw_text(f"Luck: {self.stats.luck}", column1_x, row_y - row_spacing*2, arcade.color.BLACK, 18)
        arcade.draw_text(f"Range: {self.stats.range}", column1_x, row_y - row_spacing*3, arcade.color.BLACK, 18)

        # Column 2 - Inventory
        arcade.draw_text(f"Coins: {self.stats.get_coin_number()}", column2_x, row_y, arcade.color.BLACK, 18)
        arcade.draw_text(f"Keys: {self.stats.get_key_number()}", column2_x, row_y - row_spacing, arcade.color.BLACK, 18)
        arcade.draw_text(f"Bombs: {self.stats.get_bomb_number()}", column2_x, row_y - row_spacing*2, arcade.color.BLACK, 18)
        arcade.draw_text(f"Health: {self.stats.health}", column2_x, row_y - row_spacing*3, arcade.color.BLACK, 18)

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.game_view)
        elif key == arcade.key.ENTER:  # reset game
            game = GameView(self.game_view.difficulty_options)
            game.setup()
            self.window.show_view(game)