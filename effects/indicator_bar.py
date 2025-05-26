# indicator_bar.py (Your new/updated file for this class)
import arcade
from arcade.types import Color


class IndicatorBar:
    """
    Represents a bar which can display information about a sprite.
    Adapted from Arcade's sprite_health example.
    """

    def __init__(
            self,
            owner,  # The sprite/entity owning this bar
            sprite_list: arcade.SpriteList,  # The SpriteList to add bar components to
            position: tuple[float, float] = (0, 0),
            full_color: Color = arcade.color.GREEN,
            background_color: Color = arcade.color.BLACK,
            width: int = 100,  # Base width of the fillable area (unscaled)
            height: int = 4,  # Base height of the fillable area (unscaled)
            border_size: int = 4,  # Total padding around the fillable area (e.g., 2px border on each side)
            bar_scale: float = 1.0,  # Uniform scaling factor for the bar's sprites
    ) -> None:
        self.owner = owner
        self.sprite_list: arcade.SpriteList = sprite_list

        # Store unscaled dimensions for the fillable part
        self._base_bar_width: int = width
        self._base_bar_height: int = height

        self._center_x: float = position[0]
        self._center_y: float = position[1]
        self._fullness: float = 1.0
        self._bar_scale: float = bar_scale  # Store the scale factor

        # Background box dimensions are unscaled base + border
        bg_unscaled_width = self._base_bar_width + border_size
        bg_unscaled_height = self._base_bar_height + border_size

        self._background_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            int(bg_unscaled_width),
            int(bg_unscaled_height),
            color=background_color,
        )
        # Full box uses the unscaled base dimensions
        self._full_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._base_bar_width,
            self._base_bar_height,
            color=full_color,
        )

        # Apply scale to the component sprites
        self._background_box.scale = self._bar_scale
        self._full_box.scale = self._bar_scale

        # Add to sprite list
        self.sprite_list.append(self._background_box)
        self.sprite_list.append(self._full_box)

        # Set initial position and fullness (which also aligns full_box)
        self.position = position
        self.fullness = 1.0

    def __repr__(self) -> str:
        return f"<IndicatorBar (Owner={self.owner})>"

    @property
    def background_box(self) -> arcade.SpriteSolidColor:
        return self._background_box

    @property
    def full_box(self) -> arcade.SpriteSolidColor:
        return self._full_box

    # --- Position and Fullness ---
    @property
    def position(self) -> tuple[float, float]:
        return self._center_x, self._center_y

    @position.setter
    def position(self, new_position: tuple[float, float]) -> None:
        if new_position == self.position and self._background_box and self._background_box.position == new_position:
            return  # No change

        self._center_x, self._center_y = new_position

        if not self._background_box or not self._full_box:  # Killed
            return

        # Position the center of the background box
        self._background_box.position = new_position

        # Re-apply fullness, which handles full_box alignment relative to background_box
        self._update_full_box_visuals()

    @property
    def fullness(self) -> float:
        return self._fullness

    @fullness.setter
    def fullness(self, new_fullness: float) -> None:
        # Clamp
        if not (-0.0001 <= new_fullness <= 1.0001):
            raise ValueError(f"Fullness {new_fullness} must be between 0.0 and 1.0.")
        new_fullness = max(0.0, min(1.0, new_fullness))

        if new_fullness == self._fullness:
            return  # No change

        self._fullness = new_fullness
        self._update_full_box_visuals()

    def _update_full_box_visuals(self) -> None:
        """Internal method to update the full_box's width and position."""
        if not self._background_box or not self._full_box:  # Killed
            return

        if self._fullness == 0.0:
            self.full_box.visible = False
        else:
            self.full_box.visible = True

            # Set unscaled width of the full_box based on fullness and base width
            self.full_box.width = self._base_bar_width * self._fullness

            # Align the full_box relative to the background_box
            # The full_box should be centered vertically with the background_box.
            self.full_box.center_y = self._background_box.center_y

            # The left edge of the "fillable area" (where full_box starts)
            # is offset from the background_box's left edge by the border thickness.
            # background_box.width (scaled) vs self._base_bar_width * self._bar_scale (scaled)
            # Scaled border thickness on one side:
            scaled_border_thickness_one_side = (self._background_box.width - (
                        self._base_bar_width * self._bar_scale)) / 2.0

            self.full_box.left = self._background_box.left + scaled_border_thickness_one_side

    @property
    def bar_scale(self) -> float:
        return self._bar_scale

    @bar_scale.setter
    def bar_scale(self, new_scale: float) -> None:
        if new_scale == self._bar_scale:
            return
        self._bar_scale = new_scale
        if self._background_box:
            self._background_box.scale = self._bar_scale
        if self._full_box:
            self._full_box.scale = self._bar_scale
        # Re-position/align based on new scale
        self._update_full_box_visuals()

    def kill(self) -> None:
        """Removes the indicator bar's sprites from their sprite list."""
        if self._background_box:
            self._background_box.kill()
            self._background_box = None
        if self._full_box:
            self._full_box.kill()
            self._full_box = None