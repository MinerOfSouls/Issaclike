import arcade
from pyglet.graphics import Batch

from collectables.interactive_item import InteractiveItem
from managers.collision_manager import CollisionManager

DEFAULT_FONT_SIZE = 15


class BuyableItem(InteractiveItem):
    def __init__(self, physics_engine, stats, textures, sprite_details):
        super().__init__(physics_engine, stats, textures, sprite_details)
        self.item_price = 5
        self.batch = Batch()
        self.price_text = None  # Store the text object for reuse

    def on_setup(self):
        if self.price_text is None:  # Create text only once
            self.price_text = arcade.Text(
                str(self.item_price),
                self.center_x,
                self.center_y + 20,  # Position above the item
                arcade.color.WHITE,
                DEFAULT_FONT_SIZE,
                font_name="Kenney Blocks",
            )
        self.price_text.draw()

        super().on_setup()  # Need to explicitly call parent's on_setup

        def item_player_handle(sprite_a, sprite_b, arbiter, space, data):
            if self.stats.coins >= self.item_price:
                if self.collectable:
                    item_sprite = arbiter.shapes[0]
                    item_sprite = self.physics_engine.get_sprite_for_shape(item_sprite)
                    try:
                        item_sprite.remove_from_sprite_lists()
                    except KeyError:
                        pass
                return CollisionManager.handle_effect(self.item_type, self.stats)
            return False

    def draw(self): 
        self.batch.draw()

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        super().update(delta_time, *args, **kwargs)
        # Update text position if it exists
        if self.price_text:
            self.price_text.draw()


