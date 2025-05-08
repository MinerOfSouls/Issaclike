from DamageDealer import DamageDealer


class EffectHandler:
    def __init__(self,physics_engine,stats):
        self.stats = stats
        self.physics_engine = physics_engine
        self.damage_dealer = DamageDealer(stats)

    def ignore_all_collisions(self,collision_type):
        for other_type in self.physics_engine.collision_types:
            if other_type == collision_type:
                continue  # Already handled above

            self.physics_engine.add_collision_handler(
                collision_type,
                other_type,
                begin_handler=lambda *_: False,  # Ignore all collisions
            )

    def on_setup(self):
        self.ignore_all_collisions("leaf")

    @staticmethod
    def handle_effect(effect_type, stats):
        if effect_type == 'pick_coin':
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
        elif effect_type == 'explosion':
            damage_dealer = DamageDealer()
            damage_dealer.deal_damage()
            return False
        elif effect_type == 'leaf':
            return False
        return None

