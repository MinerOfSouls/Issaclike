import arcade
from rooms import Map
from parameters import *

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.map = None

        self.physics_engine = None

    def setup(self):
        self.map = Map(2)
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.map.get_current_walls(),
            self.map.get_current_doors()
        )

    def on_draw(self) -> bool | None:
        self.clear()
        self.map.draw()
        return None

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    game.setup()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()