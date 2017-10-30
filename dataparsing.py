import itertools
from dropgenerators import *
from item import ItemType, ItemPrototype
from monster import MonsterPrototype
from stats import Stats, Stat


def _load_stats(stats):
    return Stats({
        Stat[key.upper()]: value
        for key, value
        in stats.items()
    })


class JsonDataParser:

    def __init__(self, item_data, monster_data):
        self.items = {}
        self.monsters = {}
        for item, idata in item_data.items():
            self.items[item] = self.parse_item_data(idata)
        for monster, mdata in monster_data.items():
            self.monsters[monster] = self.parse_monster_data(mdata)

    def parse_item_data(self, data):
        type = ItemType[data['type'].upper()]
        name = data['name']
        rarity = data['rarity']
        min_stats, max_stats = _load_stats(data['min_stats']), _load_stats(data['max_stats'])
        min_sockets, max_sockets = data['min_sockets'], data['max_sockets']
        min_level, max_level = data['min_level'], data['max_level']
        # TODO: Does not handle effects right now.
        return ItemPrototype(
            type, name, rarity,
            min_stats, max_stats,
            min_sockets, max_sockets,
            min_level, max_level
        )

    def parse_item_drops(self, drops):
        amount = drops.pop('max_drops')
        drops = {
            self.items[name]: chance
            for name, chance
            in drops.items()
        }
        return ItemDropGenerator(drops, num=amount)

    def parse_gem_drops(self, drops):
        return lambda: []
        amount = drops.pop('max_drops')
        inputs = []
        gem_chances = []
        # FIXME: Does not work right now, needs a way to map json keys to actual gem types.
        # FIXME: Revamp drop system regarding gemranks
        for GemType, chances in drops.items():
            inputs.append(GemDropInput(GemType, chances['rank_to_chance']))
            gem_chances.append(chances['drop_chance'])
        print(inputs, gem_chances)
        return GemDropGenerator(
            dict(zip(inputs, gem_chances)),
            num=amount
        )

    def parse_monster_data(self, data):
        name = data['name']
        min_stats, max_stats = _load_stats(data['min_stats']), _load_stats(data['max_stats'])
        min_level, max_level = data['min_level'], data['max_level']
        drop_generators = [self.parse_item_drops(data['item_drops']), self.parse_gem_drops(data['gem_drops'])]
        # TODO: Does not handle effects right now.
        return MonsterPrototype(
            name,
            min_stats, max_stats,
            min_level, max_level,
            drop_generators
        )

    def __iter__(self):
        return itertools.chain(self.items.values(), self.monsters.values())

    def __str__(self):
        return str(self.items) + '\n' + str(self.monsters)