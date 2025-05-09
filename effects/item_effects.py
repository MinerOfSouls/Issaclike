from arcade import PymunkPhysicsEngine

from collectables.interactive_item import InteractiveItem

explosion_url = "resources/images/explosion.png"
explosion_details = {
    "width": 64,
    "height": 64,
    "columns": 30,
    "count": 30,
    "speed": 0.05,
    "scale": 3,
    "looping": False,
    "collectable": False,
    "item_type": "explosion",
    "body_type": PymunkPhysicsEngine.KINEMATIC,
    "mass": 10000
}

class ItemEffects:

    @staticmethod
    def explode(physics_engine,stats,effect_list,position):
        explosion = InteractiveItem(physics_engine, stats, explosion_url, explosion_details)
        explosion.position = position
        explosion.on_setup()
        effect_list.append(explosion)