import arcade

from characters.player import Player
from rooms import Map
from parameters import *
from characters.player_controller import PlayerController
from characters.stats import PlayerStatsController
from characters.attack import Attack

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.map = None
        self.player_list = None
        self.player_sprite = None
        self.player_controller = None
        self.physics_engine = None
        self.stats = None
        self.attack = None

    def setup(self):
        self.map = Map(2)
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.map.get_current_walls(),
            self.map.get_current_doors()
        )
        self.player_list = arcade.SpriteList()
        self.player_sprite = Player("resources/images/player_sprite_placeholder.png", scale= SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        self.stats = PlayerStatsController()

        self.attack = Attack(self.player_sprite,self.stats)

        self.player_controller = PlayerController(self.player_sprite,self.stats)

    def on_draw(self) -> bool | None:
        self.clear()
        self.map.draw()
        self.player_list.draw()
        self.attack.on_draw()
        return None

    def on_update(self, delta_time):
        self.player_controller.update()
        self.player_list.update(delta_time)
        self.attack.update()

    def on_key_press(self, key, modifiers):
        self.player_controller.on_key_press(key)
        self.attack.on_key_press(key)

    def on_key_release(self, key, modifiers):
        self.player_controller.on_key_release(key)
        self.attack.on_key_release(key)

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    game.setup()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()