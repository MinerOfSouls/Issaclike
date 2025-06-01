import arcade
from arcade.examples.transitions import FadingView
from parameters import *
from views.start_screen import StartScreenView


class VictoryView(arcade.View):
    """ Class to manage the game overview """

    def on_update(self, dt):
        pass

    def on_show_view(self):
        """ Called when switching to this view"""

        self.background_color = arcade.color.BLACK

    def on_draw(self):
        """ Draw the game overview """

        self.clear()

        arcade.draw_text("Thanks for playing", screen_width / 2, screen_height / 2,

                         arcade.color.WHITE, 30, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        """ If user hits escape, go back to the main menu view """

        if key == arcade.key.SPACE:
            arcade.exit()

    def setup(self):
        """ This should set up your game and get it ready to play """

        # Replace 'pass' with the code to set up your game

        pass
