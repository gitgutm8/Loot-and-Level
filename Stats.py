import random
from collections import defaultdict, Iterable
from enum import Enum, auto


class DamageType(Enum):
    FIRE = auto()
    PLANT = auto()
    DARKNESS = auto()
    LIGHTNING = auto()
    ICE = auto()
    WATER = auto()
    TRUE_DAMAGE = auto()


class Stat(Enum):
    DAMAGE = auto()
    HP = auto()
    MAX_HP = auto()
    CRIT_CHANCE = auto()
    CRIT_BONUS = auto()
    ARMOR = auto()
    FIRE_RES = auto()
    PLANT_RES = auto()
    DARKNESS_RES = auto()
    LIGHTNING_RES = auto()
    ICE_RES = auto()
    WATER_RES = auto()


DAMAGE_TYPE_TO_RESISTANCE = {
    DamageType.FIRE     : Stat.FIRE_RES,
    DamageType.PLANT    : Stat.PLANT_RES,
    DamageType.WATER    : Stat.WATER_RES,
    DamageType.ICE      : Stat.ICE_RES,
    DamageType.DARKNESS : Stat.DARKNESS_RES,
    DamageType.LIGHTNING: Stat.LIGHTNING_RES
}


class Stats:

    def __init__(self, initial_values={}):
        self._dict = defaultdict(Stats._Stat)
        print(initial_values)
        for stat_type, val in initial_values.items():
            if isinstance(val, Iterable):
                self._dict[stat_type] = Stats._Stat(*val)
            else:
                self._dict[stat_type] = Stats._Stat(val)

    @classmethod
    def from_random_between(cls, lower, upper):
        new_stats = {}
        for stat_type, min_stat in lower:
            max_stat = upper._dict[stat_type]
            new_stats[stat_type] = (
                random.randint(min_stat.add, max_stat.add),
                random.randint(min_stat.mul, max_stat.mul),
            )
        return cls(new_stats)

    def __iadd__(self, other):
        for stat_type, val in other._dict.items():
            self._dict[stat_type] += val
        return self

    def __isub__(self, other):
        for stat_type, val in other._dict.items():
            self._dict[stat_type] -= val
        return self

    def __getitem__(self, key):
        return self._dict[key].value()

    def __iter__(self):
        return iter(self._dict.items())

    def __str__(self):
        return '\n'.join(f'{stat_type}: {val}'
                         for stat_type, val
                         in self._dict.items())

    class _Stat:

        def __init__(self, add=0, mul=1):
            self.add = add
            self.mul = mul

        def __iadd__(self, other):
            self.add += other.add
            self.mul *= other.mul
            return self

        def __isub__(self, other):
            self.add -= other.add
            self.mul /= other.mul
            return self

        def value(self):
            return self.add * self.mul

        def __str__(self):
            return f'<{self.add}, {self.mul}>'


if __name__ == '__main__':
    for s_type in Stat:
        print(s_type)
    s = Stats()
    print(vars(s))