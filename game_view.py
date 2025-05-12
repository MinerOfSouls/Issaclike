import arcade
from arcade import LRBT, PymunkPhysicsEngine

from managers.damage_manager import DamageManager
from managers.attack_manager import AttackManager
from managers.collision_manager import CollisionManager
from Ui.draw_ui import DrawUI

from characters.player import Player
from resource_manager import get_wizard_player_character
from rooms import Map
from parameters import *
from characters.player_controller import PlayerController
from characters.stats import PlayerStatsController
from characters.Abilieties.mage_special_ability import MageSpecialAbility
from collectables.pickup_factory import PickupFactory
from collectables.place_on_map import PlaceOnMap


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
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
        self.pickup_factory = None
        self.melee_attack = None
        self.effect_handler = None
        self.place_on_map = None
        self.effects_list = arcade.SpriteList()
        self.placed_items= arcade.SpriteList()
        self.difficulty_options = None
        self.attack_manager = None

        self.player_class = 0

        self.coin_list = arcade.SpriteList()
        self.pickups_list = arcade.SpriteList()

        self.camera = arcade.Camera2D(
            position=(0, 0),
            projection=LRBT(left=0, right=WINDOW_WIDTH, bottom=0, top=WINDOW_HEIGHT),
            viewport=self.window.rect
        )

    def setup(self):
        self.player_list = arcade.SpriteList()
        #player
        if self.player_class == 1:
            self.player_sprite = get_wizard_player_character()
            self.player_sprite.scale = 1
        else:
            self.player_sprite = Player("resources/images/player_sprite_placeholder.png", scale=SPRITE_SCALING)
        self.player_sprite.center_x = WINDOW_WIDTH / 2
        self.player_sprite.center_y = WINDOW_HEIGHT / 2
        self.player_list.append(self.player_sprite)

        self.stats = PlayerStatsController()
        self.damage_dealer = DamageManager(self.stats)

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
            mass=2,
            friction=1.0,
            moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
            damping=0.01,
            collision_type="player",
            max_velocity=500,
            elasticity=0.0
        )
        self.map = Map(10, self.physics_engine, self.stats)
        self.map.on_setup()
        self.UI = DrawUI(self.stats, self.map)

        self.pickups_list = self.map.get_object_list()

        self.attack_manager = AttackManager(self.physics_engine , self.player_sprite , self.stats)


        self.pickup_factory = PickupFactory(self.physics_engine, self.pickups_list, self.stats)
        self.pickup_factory.spawn_coin(100,100)
        self.pickup_factory.spawn_chest(300,300)
        self.pickup_factory.spawn_key(200,200)
        self.pickup_factory.spawn_health_potion(300,100)
        self.pickup_factory.spawn_bomb(300,200)

        self.place_on_map = PlaceOnMap(self.player_sprite,self.placed_items,self.stats, self.physics_engine)

        # self.difficulty_options = DifficultyOptions(self.physics_engine ,self.player_sprite, self.stats , self.effects_list, self.attack_manager)
        # self.difficulty_options.on_setup()

        self.effect_handler = CollisionManager(self.physics_engine, self.stats)
        self.effect_handler.on_setup()

    def on_draw(self) -> bool | None:
        self.clear()
        self.pickups_list.draw()
        self.map.draw()
        self.player_list.draw()

        if self.attack_manager.current_attack:
            self.attack_manager.current_attack.on_draw()

        self.UI.on_draw()
        self.place_on_map.on_draw()
        # self.difficulty_options.draw()

        return None

    def on_update(self, delta_time):

        if not self.map.is_loaded():
            print('enter')
            self.map.rooms[self.map.current_room].loaded = True # god xd cursed
            self.pickups_list = self.map.get_object_list()

        self.pickups_list.update()

        self.player_controller.on_update(self.physics_engine)



        self.damage_dealer.update()
        self.player_list.update(delta_time)

        if self.attack_manager.current_attack:
            self.attack_manager.current_attack.update()

        self.special_ability.update()
        self.UI.on_update()
        self.place_on_map.update()
        # self.difficulty_options.update()
        self.physics_engine.step()
        self.map.update(delta_time, self.player_sprite)


    def on_key_press(self, key, modifiers):
        self.player_controller.on_key_press(key)

        if self.attack_manager.current_attack:
            self.attack_manager.current_attack.on_key_press(key)

        self.special_ability.on_key_press(key)
        self.place_on_map.on_key_press(key)
        if key == arcade.key.ESCAPE:
            from views.pause_screen import PauseView
            pause = PauseView(self)
            self.window.show_view(pause)


    def on_key_release(self, key, modifiers):
        self.player_controller.on_key_release(key)

        if self.attack_manager.current_attack:
            self.attack_manager.current_attack.on_key_release(key)

        self.special_ability.on_key_release(key)
