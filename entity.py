from enum import Enum, auto
from stats import DamageType, Stat, DAMAGE_TYPE_TO_RESISTANCE, Stats


class BattleTrigger(Enum):
    HIT = auto()
    ROUND_START = auto()
    BATTLE_START = auto()
    HIT_BY_ENEMY = auto()
    BATTLE_END = auto()
    BATTLE_WON = auto()
    BATTLE_LOST = auto()


class Entity:

    def __init__(self, stats, effects=None):
        self.stats = stats
        self.effects = effects or []

    def receive_damage(self, amount, type):
        amount = self._calculate_damage(amount, type)
        self.remove_stats(Stats({Stat.HP: amount}))
        if self.stats[Stat.HP] <= 0:
            """self.die()"""

    def _calculate_damage(self, amount, type):
        if type == DamageType.TRUE_DAMAGE:
            return amount
        return amount - self.stats[Stat.ARMOR] - self.stats[DAMAGE_TYPE_TO_RESISTANCE[type]]

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

    def get_enemy(self):
        return self.enemy
