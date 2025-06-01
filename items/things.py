import arcade

from items.item import Item
from random import randint
from parameters import SPRITE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT
from collectables.pickup_factory import PickupType


class Repulsor(Item):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.cooldown = 8
        self.timer = 0
        self.repulsion_sprite = None
        self.radius = 0
        self.max_radius = 64
        self.active = False
        self.p_X = 0
        self.p_Y = 0

    def update(self, **kwargs):
        if self.active:
            self.timer = 0
            if self.radius >= self.max_radius:
                self.repulsion_sprite.remove_from_sprite_lists()
                self.active = False
                return
            self.radius = self.radius + 4
            self.repulsion_sprite.remove_from_sprite_lists()
            new_sprite = arcade.sprite.SpriteCircle(self.radius, arcade.color.WHITE)
            new_sprite.center_x = self.p_X
            new_sprite.center_y = self.p_Y
            kwargs["objects"].append(new_sprite)
            kwargs["engine"].add_sprite(new_sprite, body_type=2, collision_type="repulse")
            self.repulsion_sprite = new_sprite
        else:
            self.timer += kwargs["delta_time"]

    def activated(self, **kwargs):
        self.active = True
        self.repulsion_sprite = arcade.sprite.SpriteCircle(1, arcade.color.WHITE)
        self.p_X = kwargs["player"].center_x
        self.p_Y = kwargs["player"].center_y
        self.repulsion_sprite.center_x = self.p_X
        self.repulsion_sprite.center_y = self.p_Y

    def __str__(self):
        return "Repulsor"

class Wallet(Item):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.cooldown = 10
        self.timer = 0

    def update(self, **kwargs):
        self.timer += kwargs["delta_time"]
        if self.timer > self.cooldown:
            map = kwargs["map"]
            map.rooms[map.current_room].spawn_reward.pickup_factory.create_pickup(PickupType.COIN,
                randint(SPRITE_SIZE*2, WINDOW_WIDTH - SPRITE_SIZE*2),randint(SPRITE_SIZE*2, WINDOW_WIDTH - SPRITE_SIZE*2))
            self.timer = 0

    def activated(self, **kwargs):
        pass

    def __str__(self):
        return "Wallet"

class Grace(Item):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.cooldown = 1
        self.timer = 0

    def update(self, **kwargs):
        self.timer += kwargs["delta_time"]

    def activated(self, **kwargs):
        if self.timer > self.cooldown:
            map = kwargs["map"]
            engine = kwargs["engine"]
            player_sprite = kwargs["player"]
            map.rooms[map.current_room].leave()
            map.current_room = (0, 0)
            engine.set_position(player_sprite, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
            map.rooms[map.current_room].enter()
            engine.resync_sprites()
            self.timer = 0

    def __str__(self):
        return "Grace"

class Sacrifice(Item):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.cooldown = 1
        self.timer = 0

    def update(self, **kwargs):
        self.timer += kwargs["delta_time"]

    def activated(self, **kwargs):
        enemy_crl = kwargs["map"].get_enemy_controller()
        if kwargs["stats"].health > 1 and self.timer > self.cooldown and enemy_crl:
            self.timer = 0
            kwargs["stats"].health = 1
            kwargs["stats"].coins = 0
            enemy_crl.enemy_sprite_list.clear()

    def __str__(self):
        return "Sacrifice"

class Snowflake(Item):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.cooldown = 30
        self.timer = 0

    def update(self, **kwargs):
        self.timer += kwargs["delta_time"]

    def activated(self, **kwargs):
        enemy_crl = kwargs["map"].get_enemy_controller()
        if self.timer > self.cooldown and enemy_crl is not False:
            self.timer = 0
            enemy_crl.freeze = True

    def __str__(self):
        return "Snowflake"

class Totem(Item):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.used = False

    def update(self, **kwargs):
        if kwargs["stats"].health == 1 and not self.used:
            kwargs["stats"].health += 4

    def activated(self, **kwargs):
        pass

    def __str__(self):
        return "Totem"

def name_to_item(name: str) -> Item:
    match name:
        case "Repulsor": return Repulsor(arcade.SpriteCircle(10, arcade.color.WHITE))
        case "Wallet": return Wallet(arcade.SpriteCircle(10, arcade.color.BLUE))
        case "Grace": return Grace(arcade.SpriteCircle(10, arcade.color.GREEN))
        case "Sacrifice": return Sacrifice(arcade.SpriteCircle(10, arcade.color.RED))
        case "Snowflake": return Snowflake(arcade.SpriteCircle(10, arcade.color.ICEBERG))
        case "Totem": return Totem(arcade.SpriteCircle(10, arcade.color.GOLD))
        case _: raise ValueError("Invalid save / Invalid item name")

