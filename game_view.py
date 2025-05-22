import arcade
from arcade import LRBT, PymunkPhysicsEngine

from characters.Abilieties.knight_special_ability import KnightSpecialAbility
from managers.damage_manager import DamageManager
from managers.attack_manager import AttackManager
from managers.collision_manager import CollisionManager
from Ui.draw_ui import DrawUI

from characters.player import Player
from managers.difficulty_manager import DifficultyOptions
from resource_manager import get_wizard_player_character
from rooms import Map
from parameters import *
from characters.player_controller import PlayerController
from characters.stats import PlayerStatsController
from characters.Abilieties.mage_special_ability import MageSpecialAbility
from collectables.place_on_map import PlaceOnMap
from characters.Abilieties.dragon_special_ability import DragonSpecialAbility

from items.inventory import Inventory

class GameView(arcade.View):
    def __init__(self,difficulty_options):
        super().__init__()
        self.difficulty_options = difficulty_options
        self.damage_dealer = None
        self.map = None
        self.player_list = None
        self.player_sprite = None
        self.player_controller = None
        self.physics_engine: PymunkPhysicsEngine | None = None
        self.stats = None
        self.attack = None
        self.special_ability = None
        self.UI = None
        self.melee_attack = None
        self.collision_handler = None
        self.place_on_map = None
        self.effects_list = arcade.SpriteList()
        self.placed_items= arcade.SpriteList()
        self.difficulty_manager = None
        self.attack_manager = None
        self.inventory = None

        self.player_class = 0

        self.coin_list = arcade.SpriteList()
        self.pickups_list = arcade.SpriteList()

        self.camera = arcade.Camera2D(
            position=(0, 0),
            projection=LRBT(left=0, right=WINDOW_WIDTH, bottom=0, top=WINDOW_HEIGHT),
            viewport=self.window.rect
        )

        self.room_number = 10

    def setup(self):
        self.stats = PlayerStatsController()
        # physics engine setup
        damping = 0.7
        gravity = (0, 0)

        self.physics_engine = PymunkPhysicsEngine(
            damping=damping,
            gravity=gravity,
        )

        # player setup
        self.player_list = arcade.SpriteList()
        if self.player_class ==0:
            self.player_sprite = Player("resources/images/player_sprite_placeholder.png", scale=SPRITE_SCALING)
            self.special_ability = KnightSpecialAbility(self.physics_engine, self.player_sprite, self.stats)
        if self.player_class == 1:
            self.player_sprite = get_wizard_player_character()
            self.player_sprite.scale = 1
            self.special_ability = MageSpecialAbility(self.physics_engine, self.stats, self.player_sprite)
            self.special_ability.on_setup()
        elif self.player_class == 2:
            self.player_sprite = Player("resources/images/player_sprite_placeholder.png", scale=SPRITE_SCALING)
            self.special_ability = DragonSpecialAbility(self.physics_engine, self.player_sprite, self.stats,self.map)
        self.player_sprite.center_x = WINDOW_WIDTH / 2
        self.player_sprite.center_y = WINDOW_HEIGHT / 2
        self.player_list.append(self.player_sprite)
        # add player to physics_engine
        self.physics_engine.add_sprite(
            self.player_sprite,
            mass=2,
            friction=1.0,
            moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
            damping=0.01,
            collision_type="player",
            max_velocity=500,
            elasticity=0.0
        )

        self.map = Map(self.room_number, self.physics_engine, self.stats,self.special_ability)
        self.map.on_setup()


        self.damage_dealer = DamageManager(self.stats)
        # add player to physics_engine

        self.player_controller = PlayerController(self.player_sprite,self.stats)

        self.UI = DrawUI(self.stats, self.map)

        def next_level_handle(*args):
            self.map.rooms[self.map.current_room].leave()
            self.room_number = self.room_number + 1
            self.map = Map(self.room_number, self.physics_engine, self.stats)
            self.map.on_setup()

        def no_collision(*args):
            return False

        self.physics_engine.add_collision_handler("player", "stairs", post_handler=next_level_handle)
        self.physics_engine.add_collision_handler("player", "repulse", pre_handler=no_collision)
        self.pickups_list = self.map.get_object_list()

        self.attack_manager = AttackManager(self.physics_engine , self.player_sprite , self.stats)



        self.place_on_map = PlaceOnMap(self.player_sprite,self.placed_items,self.stats, self.physics_engine)

        self.difficulty_manager = DifficultyOptions(self.physics_engine ,self.player_sprite, self.stats , self.attack_manager, self.map, self.effects_list,self.difficulty_options)
        self.difficulty_manager.on_setup()

        self.collision_handler = CollisionManager(self.physics_engine, self.stats)
        self.collision_handler.on_setup()

        self.inventory = Inventory()
        self.inventory.load()


    def on_draw(self) -> bool | None:
        self.clear()
        self.map.draw()
        self.player_list.draw()
        self.special_ability.draw()

        if self.attack_manager.current_attack:
            self.attack_manager.current_attack.on_draw()

        self.UI.on_draw()
        self.place_on_map.on_draw()
        self.difficulty_manager.draw()
        self.inventory.draw()
        return None

    def on_update(self, delta_time):

        self.difficulty_manager.update()

        if not self.map.is_loaded():
            self.map.rooms[self.map.current_room].loaded = True  # god xd cursed

        self.player_controller.on_update(self.physics_engine)

        self.damage_dealer.update()
        self.player_list.update(delta_time)

        if self.attack_manager.current_attack:
            self.attack_manager.current_attack.update()

        self.special_ability.update()
        self.UI.on_update()
        self.place_on_map.update()
        self.physics_engine.step()
        self.map.update(delta_time, self.player_sprite)
        self.inventory.update(engine = self.physics_engine, delta_time = delta_time, player = self.player_sprite,
                              pickup_factory = self.pickup_factory, map = self.map, stats = self.stats)

        if self.stats.health <= 0:
            from views.game_over import GameOverView
            game_over = GameOverView()
            self.window.show_view(game_over)


    def on_key_press(self, key, modifiers):
        self.player_controller.on_key_press(key)

        if self.attack_manager.current_attack:
            self.attack_manager.current_attack.on_key_press(key)

        self.special_ability.on_key_press(key)
        self.place_on_map.on_key_press(key)
        if key == arcade.key.ESCAPE:
            self.inventory.save()
            from views.pause_screen import PauseView
            pause = PauseView(self)
            self.window.show_view(pause)

        self.inventory.on_key_press(key, engine = self.physics_engine, player = self.player_sprite,
                              pickup_factory = self.pickup_factory, map = self.map, stats = self.stats)


    def on_key_release(self, key, modifiers):
        self.player_controller.on_key_release(key)

        if self.attack_manager.current_attack:
            self.attack_manager.current_attack.on_key_release(key)

        self.special_ability.on_key_release(key)
