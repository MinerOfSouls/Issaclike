import arcade
from parameters import *

starting_room_url = "resources/images/Ui/StartinRoom.png"
enemy_room_url = "resources/images/Ui/EnemyRoom.png"
treasure_room_url = "resources/images/Ui/TreasureRoom.png"
boss_room_url ="resources/images/Ui/BossRoom.png"
unknown_room_url = "resources/images/Ui/UnknownRoom.png"

class MiniMap:
    def __init__(self, map ):
        self.width = 200
        self.height = 150
        self.margin = 10
        self.alpha = 180
        self.border_thickness = 2
        self.background_color = arcade.color.GRAY
        self.border_color = arcade.color.WHITE
        self.room_size = 32
        self.map = map

        self.current_room = self.map.current_room
        self.previous_room = None
        self.full_layout = self.map.mini_map
        self.visited_rooms = {}
        self.room_connections = self.map.connections


        # Load textures
        self.room_textures = {
            0: arcade.load_texture(starting_room_url),  # starting room
            1: arcade.load_texture(boss_room_url),  # basic room (using same as starting)
            2: arcade.load_texture(enemy_room_url),  # enemy room
            3: arcade.load_texture(treasure_room_url),  # treasure room
            4: arcade.load_texture(unknown_room_url) # unknown room
        }

    def update_mini_map(self):
        self.visited_rooms[self.current_room] = self.full_layout.get(self.current_room)

        connections = self.room_connections.get(self.current_room)
        for connected_room in connections.values():
            if connected_room not in self.visited_rooms:
                self.visited_rooms[connected_room] = 4  # Unknown

    def draw(self):
        """Draw the minimap in the top-right corner."""
        # Position calculations
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
            color=(255, 255, 255, 200),  # Semi-transparent white,
        )

        # Find map bounds
        min_x = min(x for x, y in self.full_layout.keys())
        max_x = max(x for x, y in self.full_layout.keys())
        min_y = min(y for x, y in self.full_layout.keys())
        max_y = max(y for x, y in self.full_layout.keys())

        # Calculate grid center
        center_x = (left + right) / 2
        center_y = (bottom + top) / 2

        # Calculate grid dimensions
        grid_width = (max_x - min_x + 1) * self.room_size
        grid_height = (max_y - min_y + 1) * self.room_size

        # Calculate grid starting position (top-left corner)
        grid_left = center_x - grid_width / 2
        grid_top = center_y + grid_height / 2

        # Draw each room based on the map_layout
        for (x, y), room_type in self.visited_rooms.items():
            # Convert grid coordinates to screen coordinates
            screen_x = grid_left + (x - min_x) * self.room_size
            screen_y = grid_top - (y - min_y) * self.room_size - self.room_size  # Adjusted for bottom-left origin

            # Create a rectangle for the room
            room_rect = arcade.LRBT(
                left=screen_x,
                right=screen_x + self.room_size,
                bottom=screen_y,
                top=screen_y + self.room_size

            )

            # Draw the room sprite
            arcade.draw_texture_rect(
                texture=self.room_textures[room_type],
                rect=room_rect,
                alpha=145
            )
        if self.current_room in self.visited_rooms:
            cx = grid_left + (self.current_room[0] - min_x) * self.room_size
            cy = grid_top - (self.current_room[1] - min_y) * self.room_size - self.room_size
            arcade.draw_lrbt_rectangle_outline(
                cx, cx + self.room_size, cy, cy + self.room_size,
                color=(255, 99, 71, 200),
                border_width=3,


            )

    def update(self):
        self.current_room = self.map.current_room
        if self.previous_room != self.current_room:

            self.previous_room = self.current_room
            print(self.current_room , self.previous_room)
            self.update_mini_map()
