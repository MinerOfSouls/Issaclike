import arcade
from arcade import LRBT, PymunkPhysicsEngine
from draw_ui import DrawUI

from characters.player import Player
from rooms import Map
from parameters import *
from characters.player_controller import PlayerController
from characters.stats import PlayerStatsController
from characters.attack.ranged_attack import RangedAttack
from characters.Abilieties.mage_special_ability import MageSpecialAbility
from animations.coin import Coin
from physics_handler import PhysicsHandler

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.map = None
        self.player_list = None
        self.player_sprite = None
        self.player_controller = None
        self.physics_engine: PymunkPhysicsEngine | None = None
        self.stats = None
        self.attack = None
        self.special_ability = None
        self.UI = None
        self.physics_handler = None

        self.coin_list = arcade.SpriteList()

        self.camera = arcade.Camera2D(
            position=(0, 0),
            projection=LRBT(left=0, right=WINDOW_WIDTH, bottom=0, top=WINDOW_HEIGHT),
            viewport=self.window.rect
        )
        self.coin = None


    def setup(self):
        self.player_list = arcade.SpriteList()

        #player
        self.player_sprite = Player("resources/images/player_sprite_placeholder.png", scale= SPRITE_SCALING)
        self.player_sprite.center_x = WINDOW_WIDTH / 2
        self.player_sprite.center_y = WINDOW_HEIGHT / 2
        self.player_list.append(self.player_sprite)

        self.stats = PlayerStatsController()
        self.UI = DrawUI(self.stats)

        self.special_ability = MageSpecialAbility(self.player_sprite)



        self.player_controller = PlayerController(self.player_sprite,self.stats)

        #physics engine setup
        damping = 0.7
        gravity = (0,0)
        self.physics_engine = PymunkPhysicsEngine(
            damping=damping,
            gravity=gravity,
        )
        self.physics_engine.add_sprite(
            self.player_sprite,
            friction=1.0,
            moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
            damping=0.01,
            collision_type="player",
            max_velocity=400,
            elasticity=0.0
        )
        self.map = Map(10, self.physics_engine, self.stats)
        self.map.on_setup()
        self.attack = RangedAttack(self.player_sprite, self.stats, self.physics_engine)

        self.coin = Coin(self.physics_engine,self.stats)
        self.coin.position = 200, 200
        self.coin_list.append(self.coin)
        self.coin.on_setup()
        self.physics_handler = PhysicsHandler(self.physics_engine,self.stats)
        self.physics_handler.on_setup()

    def on_draw(self) -> bool | None:
        self.clear()
        self.map.draw()
        self.player_list.draw()
        self.attack.on_draw()
        self.UI.on_draw()
        self.coin_list.draw()
        return None

    def on_update(self, delta_time):
        self.player_controller.on_update(delta_time, self.physics_engine)
        self.player_list.update(delta_time)
        self.attack.update()
        self.special_ability.update()
        self.UI.on_update()
        self.coin_list.update()
        self.physics_engine.step()
        self.map.update(self.player_sprite)


    def on_key_press(self, key, modifiers):
        self.player_controller.on_key_press(key)
        self.attack.on_key_press(key)
        self.special_ability.on_key_press(key)

    def on_key_release(self, key, modifiers):
        self.player_controller.on_key_release(key)
        self.attack.on_key_release(key)
        self.special_ability.on_key_release(key)
