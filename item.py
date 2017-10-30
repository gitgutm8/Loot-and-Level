import random
from enum import Enum, auto
from stats import Stats


class ItemType(Enum):
    WEAPON    = auto()
    BOOTS     = auto()
    HELMET    = auto()
    SHOULDERS = auto()
    LEGS      = auto()
    NECKLACE  = auto()
    RING      = auto()
    GLOVES    = auto()
    HARNESS   = auto()
    OFFHAND   = auto()


class Rarity(Enum):
    COMMON    = auto()
    RARE      = auto()
    EPIC      = auto()
    LEGENDARY = auto()
    UNIQUE    = auto()


class Item:

    def __init__(self, type, name, stats, socket_count, level, rarity, effects=None):
        self.type = type
        self.name = name
        self.stats = stats
        self.sockets = [None,] * socket_count
        self.level = level
        self.rarity = rarity
        self.effects = effects or []
        self.blessing = None

    def get_picked_up(self, who):
        self.owner = who

    def on_equip(self):
        self.owner.add_stats(self.stats)
        for effect in self.effects:
            self.owner.add_effect(effect)

    def on_unequip(self):
        self.owner.remove_stats(self.stats)
        for effect in self.effects:
            self.owner.remove_effect(effect)

    def add_stats(self, stats):
        self.owner.remove_stats(self.stats)
        self.stats += stats
        self.owner.add_stats(self.stats)

    def remove_stats(self, stats):
        self.owner.remove_stats(self.stats)
        self.stats -= stats
        self.owner.add_stats(self.stats)

    def embed_gem(self, gem):
        for idx, sock in enumerate(self.sockets):
            if sock is None:
                self.sockets[idx] = gem
                gem.on_embedding(self)
                break
        else:
            """no empty socket"""

    def remove_gem(self, idx):
        gem = self.sockets[idx]
        self.sockets[idx] = None
        gem.on_removal(self)

    def bless(self, blessing):
        if self.blessing:
            self.blessing.remove(self)
        self.blessing = blessing
        blessing.add(self)


def ItemPrototype(
    type, name, rarity,
    min_stats, max_stats,
    min_sockets, max_sockets,
    min_level, max_level,
    effect_generators=None
):
    effect_generators = effect_generators or []
    def inner():
        return Item(
            type, name,
            stats=Stats.from_random_between(min_stats, max_stats),
            socket_count=random.randint(min_sockets, max_sockets),
            level=random.randint(min_level, max_level),
            rarity=rarity,
            effects=[eg() for eg in effect_generators]
        )
    return inner


if __name__ == '__main__':
    beginner_sword = ItemPrototype(
        ItemType.WEAPON, 'Novizenschwert',Rarity.COMMON
    )