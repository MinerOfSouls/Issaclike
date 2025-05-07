import arcade

from collectables.animation import Animation
from collectables.bomb import Bomb  # Import your Bomb class


explosion_url = "resources/images/explosion.png"
explosion_details = {"width": 64,"height": 64,"columns": 30,"count": 30,"speed": 0.05,"scale": 3,"looping": False}

class PlaceOnMap:
    def __init__(self, player_sprite,placed_items,stats, physics_engine):
        self.placed_items = placed_items
        self.effects = arcade.SpriteList()
        self.player_sprite = player_sprite
        self.physics_engine = physics_engine
        self.stats = stats

    def place_item(self, item):
        if self.stats.bombs >0:
            item.position = self.player_sprite.center_x, self.player_sprite.center_y
            item.on_setup()
            self.placed_items.append(item)
            self.stats.bombs -=1

    def spawn_bomb(self):
        bomb_sprite = Bomb(self.physics_engine, self.stats)
        self.place_item(bomb_sprite)

    def update(self, delta_time: float = 1/60):
        self.placed_items.update()
        self.effects.update()
        for bomb in self.placed_items:
            if bomb.timeout <0:
                explosion = Animation(explosion_url,explosion_details)
                explosion.position = bomb.center_x , bomb.center_y
                self.effects.append(explosion)
                self.placed_items.remove(bomb)

    def on_draw(self):
        self.placed_items.draw()
        self.effects.draw()

    def on_key_press(self, key):
        if key == arcade.key.E:
            self.spawn_bomb()  # Use spawn_bomb() on press

