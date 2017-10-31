from stats import DamageType, Stat, DAMAGE_TYPE_TO_RESISTANCE, Stats


class Entity:

    def __init__(self, stats, effects=None):
        self.stats = stats
        self.effects = effects or []
        self.battle_wrappers = []

    def receive_damage(self, amount, type):
        amount = self._calculate_damage(amount, type)
        self.remove_stats(Stats({Stat.HP: amount}))
        return amount

    def _calculate_damage(self, amount, type):
        if type == DamageType.TRUE_DAMAGE:
            return amount
        return amount - self.stats[Stat.ARMOR] - self.stats[DAMAGE_TYPE_TO_RESISTANCE[type]]

    def add_battle_wrapper(self, bw):
        self.battle_wrappers.append(bw)

    def remove_battle_wrapper(self, bw):
        self.battle_wrappers.remove(bw)

    def prepare_battle_wrappers(self):
        for bw in self.battle_wrappers:
            bw.prepare(self)

    def cleanup_battle_wrappers(self):
        for bw in self.battle_wrappers:
            bw.cleanup(self)

    def alive(self):
        return self.stats[Stat.HP] > 0

    def heal(self, amount):
        amount = min(amount, self.missing_hp())
        self.add_stats(Stats({Stat.HP: amount}))

    def missing_hp(self):
        return self.stats.get(Stat.MAX_HP) - self.stats.get(Stat.HP)

    def add_stats(self, stats):
        self.stats += stats

    def remove_stats(self, stats):
        self.stats -= stats

    def on_trigger(self, trigger):
        for effect in self.effects:
            if effect.trigger == trigger:
                effect.apply()

    def add_effect(self, effect):
        self.effects.append(effect)

    def remove_effect(self, effect):
        self.effects.remove(effect)

    def has_effect(self, effect):
        return effect in self.effects
