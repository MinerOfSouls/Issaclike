from parameters import *
from views.character_selection import CharacterSelection

arcade.resources.load_kenney_fonts()


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.stats = game_view.stats  # Assuming player_stats is accessible from game_view
        self.background = arcade.load_texture("resources/images/pause_screen.png")

    def on_show_view(self):
        self.window.background_color = arcade.color.ORANGE

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0, 0, screen_width, screen_height),
        )

        # Draw controls info
        arcade.draw_text("Press P to resume | ENTER to restart | ESC to quit",
                         screen_width / 2.1,
                         screen_height / 1.40,
                         arcade.color.WHITE,
                         font_size=60,
                         anchor_x="center",
                         font_name="Kenney Pixel")

        # Draw stats box
        stats_left = screen_width / 3
        stats_top = screen_height / 1.6
        stats_width = screen_width / 3

        # Draw stats in two columns
        column1_x = stats_left + 30
        column2_x = stats_left + stats_width / 2 + 30
        row_y = stats_top - 70
        row_spacing = 60

        # Column 1 - Core stats
        arcade.draw_text(f"Speed: {self.stats.speed}", column1_x, row_y, arcade.color.WHITE, 48,
                         font_name="Kenney Pixel")
        arcade.draw_text(f"Damage: {self.stats.damage}", column1_x, row_y - row_spacing, arcade.color.WHITE, 48,
                         font_name="Kenney Pixel")
        arcade.draw_text(f"Luck: {self.stats.luck}", column1_x, row_y - row_spacing * 2, arcade.color.WHITE, 48,
                         font_name="Kenney Pixel")
        arcade.draw_text(f"Range: {self.stats.range}", column1_x, row_y - row_spacing * 3, arcade.color.WHITE, 48,
                         font_name="Kenney Pixel")

        # Column 2 - Inventory
        arcade.draw_text(f"Coins: {self.stats.get_coin_number()}", column2_x, row_y, arcade.color.WHITE, 48,
                         font_name="Kenney Pixel")
        arcade.draw_text(f"Keys: {self.stats.get_key_number()}", column2_x, row_y - row_spacing, arcade.color.WHITE, 48,
                         font_name="Kenney Pixel")
        arcade.draw_text(f"Bombs: {self.stats.get_bomb_number()}", column2_x, row_y - row_spacing * 2,
                         arcade.color.WHITE, 48, font_name="Kenney Pixel")
        arcade.draw_text(f"Health: {self.stats.health}", column2_x, row_y - row_spacing * 3, arcade.color.WHITE, 48,
                         font_name="Kenney Pixel")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.P:  # resume game
            self.window.show_view(self.game_view)
        elif key == arcade.key.ENTER:  # reset game
            character_selection = CharacterSelection()
            self.window.show_view(character_selection)
        elif key == arcade.key.ESCAPE:
            arcade.exit()
