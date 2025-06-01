from enums.pickup_type import PickupType
from collectables.base.interactive_item import InteractiveItem
from resource_manager import get_object
from enum import Enum, auto


class PickupFactory:
    def __init__(self, physics_engine, pickups_list, stats):
        self.pickups_list = pickups_list
        self.physics_engine = physics_engine
        self.stats = stats
        self._item_creators = {
            PickupType.COIN: self._create_coin,
            PickupType.KEY: self._create_key,
            PickupType.BOMB: self._create_bomb,
            PickupType.HEALTH_POTION: self._create_health_potion,
            PickupType.DAMAGE_POTION: self._create_damage_potion,
            PickupType.RANGE_POTION: self._create_range_potion,
            PickupType.SPEED_POTION: self._create_speed_potion,
        }

    def create_pickup(self, pickup_type: PickupType, x: int, y: int):
        creator = self._item_creators.get(pickup_type)
        if not creator:
            raise ValueError(f"Unknown pickup type: {pickup_type}")

        item = creator(x, y)
        self._add_to_pickups_list(item)
        return item

    def _add_to_pickups_list(self, item):
        self.pickups_list.append(item)
        item.on_setup()

    def _create_coin(self, x: int, y: int):
        sprite = get_object("coin")
        coin = InteractiveItem(self.physics_engine, self.stats, sprite[0], sprite[1])
        coin.position = x, y
        return coin

    def _create_key(self, x: int, y: int):
        sprite = get_object("key")
        key = InteractiveItem(self.physics_engine, self.stats, sprite[0], sprite[1])
        key.position = x, y
        return key

    def _create_bomb(self, x: int, y: int):
        sprite = get_object("bomb")
        bomb = InteractiveItem(self.physics_engine, self.stats, sprite[0], sprite[1])
        bomb.position = x, y
        return bomb

    def _create_health_potion(self, x: int, y: int):
        sprite = get_object("health_potion")
        potion = InteractiveItem(self.physics_engine, self.stats, sprite[0], sprite[1])
        potion.position = x, y
        return potion

    def _create_damage_potion(self, x: int, y: int):
        sprite = get_object("damage_potion")
        potion = InteractiveItem(self.physics_engine, self.stats, sprite[0], sprite[1])
        potion.position = x, y
        return potion

    def _create_range_potion(self, x: int, y: int):
        sprite = get_object("range_potion")
        potion = InteractiveItem(self.physics_engine, self.stats, sprite[0], sprite[1])
        potion.position = x, y
        return potion

    def _create_speed_potion(self, x: int, y: int):
        sprite = get_object("speed_potion")
        potion = InteractiveItem(self.physics_engine, self.stats, sprite[0], sprite[1])
        potion.position = x, y
        return potion
