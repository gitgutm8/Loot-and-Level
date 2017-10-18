import collections
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
    DamageType.FIRE: Stat.FIRE_RES,
    DamageType.PLANT: Stat.PLANT_RES,
    DamageType.WATER: Stat.WATER_RES,
    DamageType.ICE: Stat.ICE_RES,
    DamageType.DARKNESS: Stat.DARKNESS_RES,
    DamageType.LIGHTNING: Stat.LIGHTNING_RES
}


class Stats:

    def __init__(self, initial_values={}):
        self._dict = {}
        for stat_type in Stat:
            self._dict[stat_type] = Stats._Stat()
        for stat_type, val in initial_values.items():
            if isinstance(val, collections.Iterable):
                self._dict[stat_type] = Stats._Stat(*val)
            else:
                self._dict[stat_type] = Stats._Stat(val)

    def __iadd__(self, other):
        for stat_type in Stat:
            self._dict[stat_type] += other._dict[stat_type]
        return self

    def __isub__(self, other):
        for stat_type in Stat:
            self._dict[stat_type] -= other._dict[stat_type]
        return self

    def get(self, stat_type):
        return self._dict[stat_type].value()

    def __getitem__(self, key):
        return self.get(key)

    def __str__(self):
        return '\n'.join(f'{stat_type}: {val}'
                         for stat_type, val
                         in vars(self).items())

    class _Stat:

        def __init__(self, add=0, mul=1):
            self.add = add
            self.mul = mul

        def __iadd__(self, other):
            self.change_add(other.add)
            self.change_mul(other.mul)
            return self

        def __isub__(self, other):
            self.change_add(-other.add)
            self.change_mul(1/other.mul)
            return self

        def change_add(self, amount):
            self.add += amount

        def change_mul(self, amount):
            self.mul *= amount

        def value(self):
            return self.add * self.mul

        def __str__(self):
            return str(self.value())


if __name__ == '__main__':
    for s_type in Stat:
        print(s_type)
    s = Stats()
    print(vars(s))