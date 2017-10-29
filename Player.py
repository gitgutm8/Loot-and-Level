from collections import Iterable
from enum import Enum, auto
from item import ItemType
from entity import Entity
from stats import *



class Inventory:

    def __init__(self, size=100, content=None):
        self.content = content or []
        self.size = size

    def add(self, items):
        if len(self.content) + len(items) < self.size:
            self.content.extend(items)

    def remove(self, item):
        self.content.remove(item)


class EntityLevel:

    def __init__(self, entity, first_xp, xp_rule, max_level, start_xp=0, start_level=1):
        self.entity = entity
        self.needed_xp = first_xp
        self.xp_rule = xp_rule
        self.max_level = max_level
        self.current_xp = start_xp
        self.current_level = start_level

    def increase_xp(self, amount):
        self.current_xp += amount
        if self.current_xp >= self.needed_xp:
            self.current_xp -= self.needed_xp
            self.current_level += 1
            self.needed_xp = self.xp_rule(self.current_level)
            self.entity.level_up()


class Player(Entity):

    def __init__(self, stats):
        super().__init__(stats)
        self.inventory = Inventory()
        self.level = EntityLevel(self, 100, lambda lvl: 100*lvl, 99)
        self.item_slots = {
            ItemType.WEAPON: None,
            ItemType.HARNESS: None,
            ItemType.HELMET: None,
            ItemType.GLOVES: None,
            ItemType.LEGS: None,
            ItemType.BOOTS: None,
            ItemType.NECKLACE: None,
            ItemType.RING: None,
            ItemType.OFFHAND: None
        }

    def pick_up(self, items):
        if not isinstance(items, Iterable):
            items = (items,)
        self.inventory.add(items)

    def combine_gems(self, g1, g2, g3):
        if all(type(g) == type(g1) and g.rank == g1.rank for g in (g2, g3)):
            g1.rank_up()
            self.inventory.remove(g2)
            self.inventory.remove(g3)

    def level_up(self):
        pass

    def equip(self, item):
        previous_item = self.item_slots[item.type]
        if previous_item is not None:
            previous_item.on_unequip()
            self.inventory.add(previous_item)
        item.on_equip()
        self.inventory.remove(item)

    def __str__(self):
        return str(self.stats)




if __name__ == '__main__':
    from Items import Item
    from Stats import Stat, Stats, Stat
    item = Item(ItemType.WEAPON, 0, 0, Stats({Stat.DAMAGE: 3}), [], 0, 0)
    player = Player(Stats(), Inventory(content=[item]))
    print(player.inventory.content)
    #print(player.stats)
    player.equip(item)
    #print(player.stats)
    print(player.stats.__sizeof__())
