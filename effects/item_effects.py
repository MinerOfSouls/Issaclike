from arcade import PymunkPhysicsEngine

from collectables.interactive_item import InteractiveItem
from resource_manager import get_object


class ItemEffects:

    @staticmethod
    def explode(physics_engine,stats,effect_list,position):
        sprite = get_object("explosion")
        explosion = InteractiveItem(physics_engine, stats, sprite[0], sprite[1])
        explosion.position = position
        explosion.on_setup()
        effect_list.append(explosion)

    @staticmethod
    def item_spawn_effect(physics_engine,stats,effect_list,position,scale):
        sprite = get_object("spawn_effect")

        sprite[1]["scale"] = scale
        hit_effect = InteractiveItem(physics_engine, stats, sprite[0], sprite[1])
        hit_effect.position = position
        hit_effect.on_setup()
        effect_list.append(hit_effect)