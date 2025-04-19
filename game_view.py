import arcade
from arcade import LRBT
from draw_ui import DrawUI

from characters.player import Player
from rooms import Map
from parameters import *
from characters.player_controller import PlayerController
from characters.stats import PlayerStatsController
from characters.attack.ranged_attack import RangedAttack
from characters.Abilieties.mage_special_ability import MageSpecialAbility

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
        self.special_ability = None
        self.colliders = None
        self.UI = None

        self.camera = arcade.Camera2D(
            position=(0, 0),
            projection=LRBT(left=0, right=WINDOW_WIDTH, bottom=0, top=WINDOW_HEIGHT),
            viewport=self.window.rect
        )


    def setup(self):
        self.map = Map(10)
        self.player_list = arcade.SpriteList()
        self.player_sprite = Player("resources/images/player_sprite_placeholder.png", scale= SPRITE_SCALING)
        self.player_sprite.center_x = WINDOW_WIDTH / 2
        self.player_sprite.center_y = WINDOW_HEIGHT / 2
        self.player_list.append(self.player_sprite)
        self.stats = PlayerStatsController()
        self.UI = DrawUI(self.stats)

        self.special_ability = MageSpecialAbility(self.player_sprite)

        self.attack = RangedAttack(self.player_sprite,self.stats)

        self.player_controller = PlayerController(self.player_sprite,self.stats)

        self.colliders = self.map.get_coliders()

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            self.colliders
        )

    def on_draw(self) -> bool | None:
        self.clear()
        self.map.draw()
        self.player_list.draw()
        self.attack.on_draw()
        self.UI.on_draw()
        return None

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_controller.update()
        self.player_list.update(delta_time)
        self.attack.update()
        self.special_ability.update()
        self.map.change_room(self.player_sprite)
        self.UI.on_update()

    def on_key_press(self, key, modifiers):
        self.player_controller.on_key_press(key)
        self.attack.on_key_press(key)
        self.special_ability.on_key_press(key)

    def on_key_release(self, key, modifiers):
        self.player_controller.on_key_release(key)
        self.attack.on_key_release(key)
        self.special_ability.on_key_release(key)
