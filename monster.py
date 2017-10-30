import random
from collections import Iterable
from entity import Entity
from stats import Stats, Stat
from functools import reduce


class Monster(Entity):

    def __init__(self, level, drops, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.level = level
        self.drops = drops
        self.name = name

    def __str__(self):
        return f"""\
Name: {self.name}
Level: {self.level}
HP: {self.stats[Stat.HP]}
Schaden: {self.stats[Stat.DAMAGE]}
"""

def MonsterPrototype(
    name,
    min_stats, max_stats,
    min_level, max_level,
    drop_generators=None,
    effect_generators=None
):
    drop_generators = drop_generators or []
    effect_generators = effect_generators or []
    def inner():
        drops = list(reduce(lambda a, b: a+b, [dg() for dg in drop_generators]))
        return Monster(
            level=random.randint(min_level, max_level),
            drops=drops,
            name=name,
            stats=Stats.from_random_between(min_stats, max_stats),
            effects=[eg() for eg in effect_generators]
        )
    return inner


if __name__ == '__main__':
    pass
