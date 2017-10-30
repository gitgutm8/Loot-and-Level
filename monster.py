import random
from collections import Iterable
from entity import Entity
from stats import Stats, Stat


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
        return Monster(
            level=random.randint(min_level, max_level),
            drops=[dg() for dg in drop_generators],
            name=name,
            stats=Stats.from_random_between(min_stats, max_stats),
            effects=[eg() for eg in effect_generators]
        )
    return inner


if __name__ == '__main__':
    from stats import Stats, Stat
    import json



    with open('monster_data.json', 'rt') as f:
        monsters = json.load(f)

    monster_prototypes = {}
    for name, m in monsters.items():
        ancestor = m['inherits']
        if ancestor:
            ancestor = monsters[ancestor]
            for key, value in ancestor.items():
                if key not in m:
                    m[key] = value
        min_stats = load_stats(m['min_stats'])
        max_stats = load_stats(m['max_stats'])
        monster_prototypes[name] = MonsterPrototype(
            m['name'],
            min_stats,
            max_stats,
            m['min_level'],
            m['max_level'],
        )
    spider = monster_prototypes['big_spider']()
    print(spider)
