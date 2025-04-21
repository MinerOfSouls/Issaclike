import arcade
from views.start_screen import StartScreenView
from parameters import *

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    start_screen = StartScreenView()
    window.show_view(start_screen)
    arcade.run()

if __name__ == "__main__":
    main()