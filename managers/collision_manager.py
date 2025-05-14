from managers.damage_manager import DamageManager


class CollisionManager:
    def __init__(self,physics_engine,stats):
        self.stats = stats
        self.physics_engine = physics_engine
        self.damage_dealer = DamageManager(stats)

    def ignore_all_collisions(self,collision_type):
        for other_type in self.physics_engine.collision_types:
            if other_type == collision_type:
                continue

            self.physics_engine.add_collision_handler(
                collision_type,
                other_type,
                begin_handler=lambda *_: False,  # Ignore all collisions
            )

    def on_setup(self):
        self.ignore_all_collisions("leaf")
        self.ignore_all_collisions("spawn_indicator")

    @staticmethod
    def handle_effect(effect_type, stats):
        if effect_type == 'explosion':
            damage_dealer = DamageManager()
            damage_dealer.deal_damage()
            return False
        elif effect_type == 'pick_coin':
            stats.coins+=1
            return True
        elif effect_type == 'pick_key':
            stats.keys += 1
            return True
        elif effect_type == 'pick_bomb':
            stats.bombs += 1
            return True
        elif effect_type == 'pick_health_potion':
            stats.health+=1
            return True
        elif effect_type == 'pick_speed_potion':
            stats.speed+=1
            return True
        elif effect_type == 'pick_range_potion':
            stats.range+=1
            return True
        elif effect_type == 'pick_damage_potion':
            stats.damage+=1
            return True
        elif effect_type == 'projectile':
            return False
        elif effect_type == 'placed_bomb':
            return True
        return None

