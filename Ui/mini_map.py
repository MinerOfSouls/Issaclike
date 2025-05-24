import arcade
from parameters import *

starting_room_url = "resources/images/Ui/StartinRoom.png"
enemy_room_url = "resources/images/Ui/EnemyRoom.png"
treasure_room_url = "resources/images/Ui/TreasureRoom.png"
boss_room_url = "resources/images/Ui/BossRoom.png"
unknown_room_url = "resources/images/Ui/UnknownRoom.png"


class MiniMap:
    def __init__(self, map_instance):
        self.width = 200
        self.height = 150
        self.margin = 10
        self.room_size = 32
        self.map_instance = map_instance

        # Fixed grid system - 25x25 grid
        self.grid_size = 25
        self.center_grid = self.grid_size // 2  # Center is at (12, 12) for 25x25 grid

        self.current_room = self.map_instance.current_room
        self.previous_room = None
        self.full_layout = self.map_instance.mini_map
        self.visited_rooms = {}  # Will store grid coordinates -> room_type
        self.room_connections = self.map_instance.connections

        # Load textures
        self.room_textures = {
            0: arcade.load_texture(starting_room_url),  # starting room
            1: arcade.load_texture(boss_room_url),  # boss room
            2: arcade.load_texture(enemy_room_url),  # enemy room
            3: arcade.load_texture(treasure_room_url),  # treasure room
            4: arcade.load_texture(unknown_room_url)  # unknown room
        }
        self.update_mini_map()

    def world_to_grid(self, world_coord):
        """Convert world coordinates to grid coordinates with (0,0) at center"""
        world_x, world_y = world_coord
        grid_x = world_x + self.center_grid
        grid_y = world_y + self.center_grid
        return (grid_x, grid_y)

    def grid_to_world(self, grid_coord):
        """Convert grid coordinates back to world coordinates"""
        grid_x, grid_y = grid_coord
        world_x = grid_x - self.center_grid
        world_y = grid_y - self.center_grid
        return (world_x, world_y)

    def is_valid_grid_coord(self, grid_coord):
        """Check if grid coordinate is within bounds"""
        grid_x, grid_y = grid_coord
        return 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size

    def update_mini_map(self):
        # Add current room to visited rooms
        current_grid_coord = self.world_to_grid(self.current_room)
        if self.is_valid_grid_coord(current_grid_coord):
            if self.current_room in self.full_layout:
                self.visited_rooms[current_grid_coord] = self.full_layout[self.current_room]

        # Add connected rooms as unknown
        connections = self.room_connections.get(self.current_room)
        if connections:
            for connected_room_coord in connections.values():
                connected_grid_coord = self.world_to_grid(connected_room_coord)
                if (self.is_valid_grid_coord(connected_grid_coord) and
                        connected_grid_coord not in self.visited_rooms):
                    room_type = 4
                    self.visited_rooms[connected_grid_coord] = room_type

    def draw(self):
        """Draw the minimap in the top-right corner."""
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
            border_width=2
        )

        if not self.visited_rooms:
            return

        # Calculate the visible area based on visited rooms
        visited_grid_coords = list(self.visited_rooms.keys())
        min_grid_x = min(x for x, y in visited_grid_coords)
        max_grid_x = max(x for x, y in visited_grid_coords)
        min_grid_y = min(y for x, y in visited_grid_coords)
        max_grid_y = max(y for x, y in visited_grid_coords)

        # Add some padding around the visible area
        padding = 1
        min_grid_x = max(0, min_grid_x - padding)
        max_grid_x = min(self.grid_size - 1, max_grid_x + padding)
        min_grid_y = max(0, min_grid_y - padding)
        max_grid_y = min(self.grid_size - 1, max_grid_y + padding)

        # Calculate drawing area
        center_x_bg = (left + right) / 2
        center_y_bg = (bottom + top) / 2

        visible_width = (max_grid_x - min_grid_x + 1) * self.room_size
        visible_height = (max_grid_y - min_grid_y + 1) * self.room_size

        # Scale down if too big for minimap area
        available_width = self.width - 20  # Leave some margin
        available_height = self.height - 20

        scale_x = available_width / visible_width if visible_width > available_width else 1
        scale_y = available_height / visible_height if visible_height > available_height else 1
        scale = min(scale_x, scale_y)

        actual_room_size = self.room_size * scale
        scaled_width = visible_width * scale
        scaled_height = visible_height * scale

        grid_screen_left = center_x_bg - scaled_width / 2
        grid_screen_bottom = center_y_bg - scaled_height / 2

        # Draw each visited room
        for (grid_x, grid_y), room_type in self.visited_rooms.items():
            # Only draw rooms in the visible area
            if (min_grid_x <= grid_x <= max_grid_x and
                    min_grid_y <= grid_y <= max_grid_y):

                screen_x = grid_screen_left + (grid_x - min_grid_x) * actual_room_size
                screen_y_bottom = grid_screen_bottom + (grid_y - min_grid_y) * actual_room_size

                # Create a rectangle for the room sprite
                room_rect = arcade.LRBT(
                    left=screen_x,
                    right=screen_x + actual_room_size,
                    bottom=screen_y_bottom,
                    top=screen_y_bottom + actual_room_size
                )

                # Draw the room sprite
                texture_to_draw = self.room_textures.get(room_type)
                if texture_to_draw:
                    arcade.draw_texture_rect(
                        texture=texture_to_draw,
                        rect=room_rect,
                        alpha=145
                    )

        # Highlight the current room
        current_grid_coord = self.world_to_grid(self.current_room)
        if (current_grid_coord in self.visited_rooms and
                min_grid_x <= current_grid_coord[0] <= max_grid_x and
                min_grid_y <= current_grid_coord[1] <= max_grid_y):
            grid_x, grid_y = current_grid_coord
            cx_left = grid_screen_left + (grid_x - min_grid_x) * actual_room_size
            cy_bottom = grid_screen_bottom + (grid_y - min_grid_y) * actual_room_size

            arcade.draw_lrbt_rectangle_outline(
                cx_left, cx_left + actual_room_size,
                cy_bottom, cy_bottom + actual_room_size,
                color=(255, 99, 71, 200),
                border_width=3,
            )

    def update(self):
        map_current_room_coord = self.map_instance.current_room
        if self.previous_room != map_current_room_coord:
            self.previous_room = self.current_room
            self.current_room = map_current_room_coord
            self.update_mini_map()