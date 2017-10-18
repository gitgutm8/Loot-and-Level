from enum import Enum, auto


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


class Item:

    def __init__(self, type, name, owner, stats, socket_count, level, rarity):
        self.type = type
        self.name = name
        self.owner = owner
        self.stats = stats
        self.sockets = [None,] * socket_count
        self.level = level
        self.rarity = rarity

    def embed_gem(self, gem):
        for idx, sock in enumerate(self.sockets):
            if sock is None:
                self.sockets[idx] = gem
                gem.on_embedding()
                break
        else:
            """no success"""

    def remove_gem(self, idx):
        gem = self.sockets[idx]
        self.sockets[idx] = None
        gem.on_removal()

