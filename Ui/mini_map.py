import arcade
from parameters import *

starting_room_url = "resources/images/Ui/StartinRoom.png"
enemy_room_url = "resources/images/Ui/EnemyRoom.png"
treasure_room_url = "resources/images/Ui/TreasureRoom.png"
boss_room_url ="resources/images/Ui/BossRoom.png"
unknown_room_url = "resources/images/Ui/UnknownRoom.png"


class MiniMap:
    def __init__(self, map_instance):  # Renamed map to map_instance to avoid conflict if map is a function
        self.width = 200
        self.height = 150
        self.margin = 10
        # self.alpha = 180 # Not used directly, alpha is set in draw calls
        # self.border_thickness = 2 # Not used directly
        # self.background_color = arcade.color.GRAY # Not used directly
        # self.border_color = arcade.color.WHITE # Not used directly
        self.room_size = 32
        self.map_instance = map_instance  # Using renamed parameter

        self.current_room = self.map_instance.current_room
        self.previous_room = None
        self.full_layout = self.map_instance.mini_map
        self.visited_rooms = {}
        self.room_connections = self.map_instance.connections

        # Load textures
        self.room_textures = {
            0: arcade.load_texture(starting_room_url),  # starting room
            1: arcade.load_texture(boss_room_url),  # boss room (corrected comment if type 1 is boss)
            2: arcade.load_texture(enemy_room_url),  # enemy room
            3: arcade.load_texture(treasure_room_url),  # treasure room
            4: arcade.load_texture(unknown_room_url)  # unknown room
        }
        # Initialize visited rooms with the starting room and its neighbors
        self.update_mini_map()  # Call this once at init to populate initial state

    def update_mini_map(self):
        # Ensure current room is marked as visited with its actual type
        if self.current_room in self.full_layout:  # Check if current_room is a valid key
            self.visited_rooms[self.current_room] = self.full_layout.get(self.current_room)
        else:
            # This case should ideally not happen if map generation is correct
            # and current_room is always a valid room coordinate.
            # Consider logging an error or handling it. For now, skip if invalid.
            pass

        # Reveal neighbors of the current room as unknown if not already visited
        connections = self.room_connections.get(self.current_room)
        if connections:  # Ensure connections is not None
            for connected_room_coord in connections.values():
                if connected_room_coord not in self.visited_rooms:
                    self.visited_rooms[connected_room_coord] = 4  # Mark as Unknown

    def draw(self):
        """Draw the minimap in the top-right corner."""
        # Position calculations for the minimap background
        left = WINDOW_WIDTH - self.width - self.margin
        right = WINDOW_WIDTH - self.margin
        top = WINDOW_HEIGHT - self.margin
        bottom = WINDOW_HEIGHT - self.height - self.margin

        # Draw background
        arcade.draw_lrbt_rectangle_filled(
            left, right, bottom, top,
            color=(50, 50, 50, 180),
        )

        # Draw border
        arcade.draw_lrbt_rectangle_outline(
            left, right, bottom, top,
            color=(255, 255, 255, 200),
            border_width=2  # Added border_width explicitly
        )

        if not self.full_layout:  # Don't try to draw if map layout is empty
            return

        # Find map bounds from the full layout (all potential rooms)
        min_x = min(x for x, y in self.full_layout.keys())
        max_x = max(x for x, y in self.full_layout.keys())
        min_y = min(y for x, y in self.full_layout.keys())
        max_y = max(y for x, y in self.full_layout.keys())

        # Calculate overall minimap grid center (within the background rectangle)
        center_x_bg = (left + right) / 2
        center_y_bg = (bottom + top) / 2

        # Calculate grid dimensions based on map data
        grid_pixel_width = (max_x - min_x + 1) * self.room_size
        grid_pixel_height = (max_y - min_y + 1) * self.room_size

        # Calculate grid starting position (bottom-left corner of the grid in screen coordinates)
        # This ensures the grid is centered within the minimap background area
        grid_screen_left = center_x_bg - grid_pixel_width / 2
        grid_screen_bottom = center_y_bg - grid_pixel_height / 2  # Bottom of the entire grid drawing area

        # Draw each visited room
        for (x, y), room_type in self.visited_rooms.items():
            # Convert map grid coordinates (x, y) to screen coordinates for drawing
            # X-coordinate: standard, map left to screen left
            screen_x = grid_screen_left + (x - min_x) * self.room_size

            # Y-coordinate: CHANGED FOR "UP IS UP"
            # (y - min_y) gives the room's 0-indexed row from the "bottom" of the map data.
            # We add this (scaled by room_size) to grid_screen_bottom.
            # So, map rooms with higher 'y' values will be drawn higher on the screen.
            screen_y_bottom_of_room = grid_screen_bottom + (y - min_y) * self.room_size

            # Create a rectangle for the room sprite
            room_rect = arcade.LRBT(
                left=screen_x,
                right=screen_x + self.room_size,
                bottom=screen_y_bottom_of_room,
                top=screen_y_bottom_of_room + self.room_size
            )

            # Draw the room sprite
            texture_to_draw = self.room_textures.get(room_type)
            if texture_to_draw:  # Ensure texture exists
                arcade.draw_texture_rect(
                    texture=texture_to_draw,
                    rect=room_rect,
                    alpha=145  # You can make this a class attribute if needed
                )

        # Highlight the current room
        if self.current_room in self.visited_rooms:
            # Calculate screen coordinates for the current room consistently
            cx_bottom_left = grid_screen_left + (self.current_room[0] - min_x) * self.room_size

            # Y-coordinate for current room highlight: CHANGED CONSISTENTLY
            cy_bottom_of_room = grid_screen_bottom + (self.current_room[1] - min_y) * self.room_size

            arcade.draw_lrbt_rectangle_outline(
                cx_bottom_left, cx_bottom_left + self.room_size,
                cy_bottom_of_room, cy_bottom_of_room + self.room_size,
                color=(255, 99, 71, 200),  # Tomato color, semi-transparent
                border_width=3,
            )

    def update(self):
        map_current_room_coord = self.map_instance.current_room
        if self.previous_room != map_current_room_coord:
            # For debugging, show the transition
            # print(f"Minimap: Room changed from {self.previous_room} to {map_current_room_coord}")

            self.previous_room = self.current_room  # Store old current_room as previous
            self.current_room = map_current_room_coord  # Update minimap's notion of current room
            self.update_mini_map()  # Update visited rooms and reveal neighbors