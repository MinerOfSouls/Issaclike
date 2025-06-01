import arcade
from views.character_selection import CharacterSelection
import arcade.gui
from parameters import *

start_bitton_url = "resources/images/start_button.png"
how_to_play_url = "resources/images/how_to_play.png"
exit_url = "resources/images/exit_button.png"


class StartScreenView(arcade.View):
    """ View to show instructions """

    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("resources/images/StartScreen.png")
        self.start_button = arcade.load_texture(start_bitton_url)
        self.how_to_play = arcade.load_texture(how_to_play_url)
        self.exit_button = arcade.load_texture(exit_url)
        self.manager = arcade.gui.UIManager()

        # Create buttons
        # self.knight = arcade.gui.UITextureButton(texture=self.start_button, scale=1)
        self.start_new_game = arcade.gui.UITextureButton(texture=self.start_button, scale=0.3)
        self.how_to_play = arcade.gui.UITextureButton(texture=self.how_to_play, scale=0.3)
        self.exit = arcade.gui.UITextureButton(texture=self.exit_button, scale=0.3)

        # Store buttons in a list for easier keyboard navigation
        self.buttons = [self.start_new_game, self.how_to_play, self.exit]
        self.selected_index = 0

        # Set up grid layout
        self.grid = arcade.gui.UIGridLayout(
            column_count=1, row_count=3, horizontal_spacing=50, vertical_spacing=50
        )
        self.grid.add(self.start_new_game, column=0, row=0)
        self.grid.add(self.how_to_play, column=0, row=1)
        self.grid.add(self.exit, column=0, row=2)

        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        self.anchor.add(
            anchor_x="center_x",
            anchor_y="bottom",
            align_y=screen_height / 4,
            child=self.grid,
        )

        # Button click handlers
        @self.start_new_game.event("on_click")
        def start_new_game(event):
            character_selection = CharacterSelection()
            self.window.show_view(character_selection)

        @self.how_to_play.event("on_click")
        def on_options(event):
            # Add your options view code here
            pass

        @self.exit.event("on_click")
        def on_exit(event):
            arcade.exit()

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
        x = button.center_x - button.width / 2 - 30  # Position to the left of the button
        y = button.center_y  # Center vertically with the button

        # Draw a triangle pointing to the selected button
        arcade.draw_triangle_filled(
            x, y,
            x - 10, y + 10,
            x - 10, y - 10,
            arcade.color.YELLOW
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F11:
            screen_width, screen_height = arcade.get_display_size()
            global resizable_scale
            resizable_scale = min(screen_width / WINDOW_WIDTH, screen_height / WINDOW_HEIGHT)
            print(screen_width, screen_height)
            print(resizable_scale)
            self.window.set_fullscreen(not self.window.fullscreen)

        if key == arcade.key.UP:
            # Move selection up
            self.selected_index = (self.selected_index - 1) % len(self.buttons)
        elif key == arcade.key.DOWN:
            # Move selection down
            self.selected_index = (self.selected_index + 1) % len(self.buttons)
        elif key == arcade.key.SPACE:
            # Activate the selected button
            if self.selected_index == 0:
                character_selection = CharacterSelection()
                self.window.show_view(character_selection)
            elif self.selected_index == 1:
                # todo options
                pass
            elif self.selected_index == 2:
                arcade.exit()
        elif key == arcade.key.ESCAPE:
            arcade.exit()
