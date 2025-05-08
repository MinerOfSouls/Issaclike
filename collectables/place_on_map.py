import arcade
from arcade import PymunkPhysicsEngine
from game_view import DamageDealer
from DamageDealer import DamageDealer
from collectables.EffectHandler import EffectHandler
from collectables.animation import Animation
from collectables.bomb import Bomb  # Import your Bomb class
from collectables.collectable import Collectable

explosion_url = "resources/images/explosion.png"
explosion_details = {
    "width": 64,
    "height": 64,
    "columns": 30,
    "count": 30,
    "speed": 0.05,
    "scale": 3,
    "looping": False,
    "collectable": False,
    "item_type": "explosion"
}

class PlaceOnMap:
    def __init__(self, player_sprite, placed_items, stats, physics_engine):
        self.placed_items = placed_items
        self.effects = arcade.SpriteList()
        self.player_sprite = player_sprite
        self.physics_engine = physics_engine
        self.stats = stats

    def place_item_by_player(self, item):
        if self.stats.bombs > 0:
            item.position = self.player_sprite.position
            item.on_setup()
            self.placed_items.append(item)
            self.stats.bombs -= 1

    def place_item(self,item,x,y):
        item.position = (x,y)
        item.on_setup()
        self.placed_items.append(item)

    def place_bomb(self,x,y):
        bomb_sprite = Bomb(self.physics_engine, self.stats, self.effects, self.placed_items)
        self.place_item(bomb_sprite,x,y)

    def place_bomb_by_player(self):
        bomb_sprite = Bomb(self.physics_engine, self.stats, self.effects,self.placed_items)
        self.place_item_by_player(bomb_sprite)

    def update(self, delta_time: float = 1 / 60):
        self.placed_items.update()
        self.effects.update()

        for effect in self.effects:
            if effect.should_delete:
                effect.remove_from_sprite_lists()

    def on_draw(self):
        self.placed_items.draw()
        self.effects.draw()

    def on_key_press(self, key):
        if key == arcade.key.E:
            self.place_bomb_by_player()