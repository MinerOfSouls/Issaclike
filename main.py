import arcade

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


    def setup(self):
        self.map = Map(10)
        self.player_list = arcade.SpriteList()
        self.player_sprite = Player("resources/images/player_sprite_placeholder.png", scale= SPRITE_SCALING)
        self.player_sprite.center_x = WINDOW_WIDTH / 2
        self.player_sprite.center_y = WINDOW_HEIGHT / 2
        self.player_list.append(self.player_sprite)
        self.stats = PlayerStatsController()

        self.physics_engine = arcade.PymunkPhysicsEngine()

        self.physics_engine.add_sprite(
            self.player_sprite,
            damping = self.stats.get_friction(),
            moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
            max_velocity=1000,
            body_type=0,
            collision_type="player"
        )

        self.map.update_engine(self.physics_engine)

        def door_interact_handler(*args):
            if self.map.change_room(self.player_sprite, self.physics_engine):
                return True
            else:
                return False

        self.physics_engine.add_collision_handler("player", "door", pre_handler=door_interact_handler)

        self.player_controller = PlayerController(self.player_sprite, self.stats, self.physics_engine)

        self.special_ability = MageSpecialAbility(self.player_sprite)

        self.attack = RangedAttack(self.player_sprite, self.stats, self.physics_engine)

    def on_draw(self) -> bool | None:
        self.clear()
        self.map.draw()
        self.player_list.draw()
        self.attack.on_draw()
        return None

    def on_update(self, delta_time):
        self.physics_engine.step(delta_time)
        self.physics_engine.resync_sprites()
        self.player_controller.update()
        self.player_list.update(delta_time)
        self.attack.update()
        self.special_ability.update()

    def on_key_press(self, key, modifiers):
        self.player_controller.on_key_press(key)
        self.attack.on_key_press(key)
        self.special_ability.on_key_press(key)

    def on_key_release(self, key, modifiers):
        self.player_controller.on_key_release(key)
        self.attack.on_key_release(key)
        self.special_ability.on_key_release(key)

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    game.setup()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()