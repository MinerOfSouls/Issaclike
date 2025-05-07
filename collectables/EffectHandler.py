from DamageDealer import DamageDealer


class EffectHandler:
    def __init__(self,stats):
        self.stats = stats
        self.damage_dealer = DamageDealer(stats)

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
        return None

