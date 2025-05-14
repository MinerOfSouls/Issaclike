from collectables.interactive_item import InteractiveItem
from effects.item_effects import ItemEffects
from resource_manager import get_object

bomb_url = "resources/images/granade.png"
bomb_details = {
    "width": 13,
    "height": 16,
    "columns": 1,
    "count": 1,
    "speed": 0.05,
    "scale": 2,
    "looping": False,
    "item_type": 'placed_bomb'
}


class Bomb(InteractiveItem):
    def __init__(self, physics_engine, stats, effect_list,placed_items):
        super().__init__(physics_engine, stats, get_object("placed_bomb")[0], get_object("placed_bomb")[1])
        self.physics_engine = physics_engine
        self.effect_list = effect_list
        self.placed_items = placed_items
        self.original_color = (255, 255, 255)  # Store original color
        self.color = self.original_color  # Initialize color


    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        super().update()
        self.item_lifetime += 1

        # Calculate red intensity based on remaining time (0-1)
        red_intensity =(self.item_lifetime / 70.0)

        # Interpolate between original color and full red
        red = 255  # Full red
        green = int(self.original_color[1] * (1 - red_intensity))
        blue = int(self.original_color[2] * (1 - red_intensity))

        self.color = (red, green, blue)

        if self.item_lifetime >= 70:
            # bomb hitbox still active during explosion don't know why
            self.physics_engine.remove_sprite(self)
            self.placed_items.remove(self)
            ItemEffects.explode(self.physics_engine,self.stats,self.effect_list,self.position)