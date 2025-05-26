import arcade
from pyglet.graphics import Batch


class ChargeEffects(object):
    _active_texts = []
    def __init__(self):
        pass

    @staticmethod
    def charge_circle(player_sprite ,current_charge , full_charge):
            charge_percentage = min(current_charge / full_charge, 1)

            r = min(255, int(charge_percentage * 255))
            g = min(255, int((1 - charge_percentage) * 255))
            b = 0

            # Set circle position to be near the player
            circle_x = player_sprite.center_x + 20
            circle_y = player_sprite.center_y + 20

            # Draw background circle (outline)
            arcade.draw_circle_outline(
                circle_x, circle_y,
                radius=10,
                color=(100, 100, 100),
                border_width=2
            )

            end_angle = 360 * charge_percentage

            arcade.draw_arc_filled(
                circle_x, circle_y,
                width=20,
                height=20,
                color=(r, g, b, 180),
                start_angle=0,
                end_angle=end_angle
            )
    @staticmethod
    def hit_effect(sprite):
        red = 255  # Full red


        sprite.color = (red, 0, 0)

    @staticmethod
    def clean_damage_indicator(sprite):
        sprite.color =  (255,255,255)


    @staticmethod
    def show_damage(batch, enemy_sprite, damage):
        text_x = enemy_sprite.center_x
        text_y = enemy_sprite.center_y + enemy_sprite.height / 2 + 10  # Position above the enemy

        damage_text_sprite = arcade.Text(
            text=str(damage),
            x=text_x,
            y=text_y,
            color=arcade.color.WHITE,  # Or arcade.color.RED for more visibility
            font_size=32,  # Drastically reduced font size
            font_name="Kenney Blocks",  # Make sure this font is available
            anchor_x="center",
            batch=batch  # Associate this text with the drawing batch
        )

        # Add to our list for timed removal
        return damage_text_sprite
    @staticmethod
    def update(delta_time):
        """
        Updates all active effects, like damage text timers.
        Call this every frame from your main game update or controller update.
        """
        # Iterate backwards because we might remove items from the list
        for i in range(len(ChargeEffects._active_texts) - 1, -1, -1):
            item = ChargeEffects._active_texts[i]
            item["timer"] -= delta_time
            if item["timer"] <= 0:
                # Timer expired, remove the text
                # kill() removes it from any sprite lists and the batch it was added to
                ChargeEffects._active_texts.pop(i)