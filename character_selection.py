import arcade
from game_view import GameView
import arcade.gui


class CharacterSelection(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        # Create buttons
        self.knight = arcade.gui.UIFlatButton(text="Knight", width=100)
        self.mage = arcade.gui.UIFlatButton(text="Mage", width=100)
        self.dragon = arcade.gui.UIFlatButton(text="Dragon", width=100)

        # Store buttons in a list for easier keyboard navigation
        self.buttons = [self.knight, self.mage, self.dragon]
        self.selected_index = 0

        # Set up grid layout
        self.grid = arcade.gui.UIGridLayout(
            column_count=3, row_count=1, horizontal_spacing=20, vertical_spacing=20
        )
        self.grid.add(self.knight, column=0, row=0)
        self.grid.add(self.mage, column=1, row=0)
        self.grid.add(self.dragon, column=2, row=0)

        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.grid,
        )

        # Button click handlers
        @self.knight.event("on_click")
        def choose_knight(event):
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        @self.mage.event("on_click")
        def choose_mage(event):
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        @self.dragon.event("on_click")
        def choose_dragon(event):
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

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
        x = button.center_x
        y = button.center_y - button.width /2 -15

        arcade.draw_triangle_filled(
            x, y,
            x + 10, y,
            x +5, y +10,
            arcade.color.YELLOW
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.selected_index = (self.selected_index - 1) % len(self.buttons)
        elif key == arcade.key.RIGHT:
            self.selected_index = (self.selected_index + 1) % len(self.buttons)
        elif key == arcade.key.SPACE:
            # Activate the selected button
            if self.selected_index == 0:
                game_view = GameView()
                game_view.setup()
                self.window.show_view(game_view)
            elif self.selected_index == 1:
                game_view = GameView()
                game_view.setup()
                self.window.show_view(game_view)
            elif self.selected_index == 2:
                game_view = GameView()
                game_view.setup()
                self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:
            from start_screen import StartScreenView
            start_screen = StartScreenView()
            self.window.show_view(start_screen)