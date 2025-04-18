import arcade
from character_selection import CharacterSelection
import arcade.gui


class StartScreenView(arcade.View):
    """ View to show instructions """

    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        # Create buttons
        self.start_new_game = arcade.gui.UIFlatButton(text="Start New Game", width=200)
        self.options = arcade.gui.UIFlatButton(text="Options", width=200)
        self.exit = arcade.gui.UIFlatButton(text="Exit", width=200)

        # Store buttons in a list for easier keyboard navigation
        self.buttons = [self.start_new_game, self.options, self.exit]
        self.selected_index = 0

        # Set up grid layout
        self.grid = arcade.gui.UIGridLayout(
            column_count=1, row_count=3, horizontal_spacing=50, vertical_spacing=50
        )
        self.grid.add(self.start_new_game, column=0, row=0)
        self.grid.add(self.options, column=0, row=1)
        self.grid.add(self.exit, column=0, row=2)

        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.grid,
        )

        # Button click handlers
        @self.start_new_game.event("on_click")
        def start_new_game(event):
            character_selection = CharacterSelection()
            self.window.show_view(character_selection)

        @self.options.event("on_click")
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