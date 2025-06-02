import arcade.gui
from parameters import *

CHARACTER_WIDTH = WINDOW_WIDTH / 3
CHARACTER_HEIGHT = WINDOW_HEIGHT / 2
DIFFICULTY_WIDTH = WINDOW_WIDTH / 8

empty_checkbox_url = "resources/images/checkbox_empty.png"
filled_checkbox_url = "resources/images/checkbox_filled.png"
knight_url = "resources/images/characters/knight_idle.png"
mage_url = "resources/images/characters/wizard_idle.png"
dragon_url = "resources/images/characters/dragon_idle (Edited).png"


class CharacterSelection(arcade.View):
    def __init__(self):

        super().__init__()
        self.background = arcade.load_texture("resources/images/character_select.png")

        self.empty_checkbox_texture = arcade.load_texture(empty_checkbox_url)
        self.filled_checkbox_texture = arcade.load_texture(filled_checkbox_url)
        self.knight_texture = arcade.load_texture(knight_url)
        self.mage_texture = arcade.load_texture(mage_url)
        self.dragon_texture = arcade.load_texture(dragon_url)

        self.manager = arcade.gui.UIManager()
        self.difficulty_options = {"wind": False, "explosions": False, "moving_fire": False, "weapon_change": False}

        # Create buttons
        self.knight = arcade.gui.UITextureButton(texture=self.knight_texture, scale=1)
        self.mage = arcade.gui.UITextureButton(texture=self.mage_texture, scale=2)
        self.dragon = arcade.gui.UITextureButton(texture=self.dragon_texture, scale=2)

        self.wind_button = arcade.gui.UITextureButton(texture=self.empty_checkbox_texture)
        self.explosions_button = arcade.gui.UITextureButton(texture=self.empty_checkbox_texture)
        self.moving_fire_button = arcade.gui.UITextureButton(texture=self.empty_checkbox_texture)
        self.random_weapons_button = arcade.gui.UITextureButton(texture=self.empty_checkbox_texture)

        # Store buttons in a list for easier keyboard navigation
        self.buttons = [self.knight, self.mage, self.dragon, self.wind_button, self.explosions_button,
                        self.moving_fire_button, self.random_weapons_button]
        self.selected_index = 0

        # Set up grid layout
        self.grid1 = arcade.gui.UIGridLayout(
            column_count=3, row_count=1, horizontal_spacing=500, vertical_spacing=100
        )
        self.grid1.add(self.knight, column=0, row=0)
        self.grid1.add(self.mage, column=1, row=0)
        self.grid1.add(self.dragon, column=2, row=0)

        self.grid2 = arcade.gui.UIGridLayout(
            column_count=8, row_count=1, horizontal_spacing=20, vertical_spacing=20
        )
        self.grid2.add(self.wind_button, column=0, row=0)
        self.grid2.add(arcade.gui.UILabel(text="Wind"), column=1, row=0, font_name="Kenney Pixel")
        self.grid2.add(self.explosions_button, column=2, row=0)
        self.grid2.add(arcade.gui.UILabel(text="Random explosions"), column=3, row=0, font_name="Kenney Pixel")
        self.grid2.add(self.moving_fire_button, column=4, row=0)
        self.grid2.add(arcade.gui.UILabel(text="Relentless fire"), column=5, row=0, font_name="Kenney Pixel")
        self.grid2.add(self.random_weapons_button, column=6, row=0)
        self.grid2.add(arcade.gui.UILabel(text="Random weapon"), column=7, row=0, font_name="Kenney Pixel")

        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        self.anchor.add(
            align_y=screen_height * 0.3,
            anchor_x="center_x",
            anchor_y="bottom",
            child=self.grid1,
        )
        self.anchor.add(
            align_y=100,
            anchor_x="center_x",
            anchor_y="bottom",
            child=self.grid2,
        )

    def on_show_view(self):
        self.window.background_color = arcade.csscolor.DARK_SLATE_BLUE
        self.window.default_camera.use()
        self.manager.enable()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0, 0, screen_width, screen_height),
        )

        self.manager.draw()

        # Draw the selection indicator (an arrow)
        button = self.buttons[self.selected_index]
        # Get the button position
        x = button.center_x
        y = button.center_y - button.width / 2 - 10

        arcade.draw_triangle_filled(
            x, y,
            x + 10, y,
            x + 5, y + 10,
            arcade.color.YELLOW
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.selected_index = (self.selected_index - 1) % len(self.buttons)
        elif key == arcade.key.RIGHT:
            self.selected_index = (self.selected_index + 1) % len(self.buttons)
        elif key == arcade.key.UP:
            self.selected_index = 0
        elif key == arcade.key.DOWN:
            self.selected_index = 3
        elif key == arcade.key.SPACE:
            # Activate the selected button
            match self.selected_index:
                case 0:
                    from views.game_view import GameView
                    game_view = GameView(self.difficulty_options)
                    game_view.player_class = 0
                    game_view.setup()
                    self.window.show_view(game_view)
                case 1:
                    from views.game_view import GameView
                    game_view = GameView(self.difficulty_options)
                    game_view.player_class = 1
                    game_view.setup()
                    self.window.show_view(game_view)
                case 2:
                    from views.game_view import GameView
                    game_view = GameView(self.difficulty_options)
                    game_view.player_class = 2
                    game_view.setup()
                    self.window.show_view(game_view)
                case 3:
                    self.difficulty_options["wind"] = not self.difficulty_options.get("wind")
                    if self.difficulty_options["wind"]:
                        self.wind_button.texture = self.filled_checkbox_texture
                    else:
                        self.wind_button.texture = self.empty_checkbox_texture
                case 4:
                    self.difficulty_options["explosions"] = not self.difficulty_options.get("explosions")
                    if self.difficulty_options["explosions"]:
                        self.explosions_button.texture = self.filled_checkbox_texture
                    else:
                        self.explosions_button.texture = self.empty_checkbox_texture
                case 5:
                    self.difficulty_options["moving_fire"] = not self.difficulty_options.get("moving_fire")
                    if self.difficulty_options["moving_fire"]:
                        self.moving_fire_button.texture = self.filled_checkbox_texture
                    else:
                        self.moving_fire_button.texture = self.empty_checkbox_texture
                case 6:
                    self.difficulty_options["weapon_change"] = not self.difficulty_options.get("weapon_change")
                    if self.difficulty_options["weapon_change"]:
                        self.random_weapons_button.texture = self.filled_checkbox_texture
                    else:
                        self.random_weapons_button.texture = self.empty_checkbox_texture

        elif key == arcade.key.ESCAPE:
            from views.start_screen import StartScreenView
            start_screen = StartScreenView()
            self.window.show_view(start_screen)
