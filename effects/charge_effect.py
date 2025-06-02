import arcade


class ChargeEffects(object):
    _active_texts = []

    def __init__(self):
        pass

    @staticmethod
    def charge_circle(player_sprite, current_charge, full_charge):
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
        sprite.color = (255, 255, 255)
