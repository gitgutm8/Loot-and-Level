from enum import Enum, auto
from Items import ItemType
from Stats import *


class Trigger(Enum):
    HIT = auto()
    ROUND_START = auto()
    BATTLE_START = auto()
    HIT_BY_ENEMY = auto()
    BATTLE_END = auto()
    BATTLE_WON = auto()
    BATTLE_LOST = auto()


class Inventory:

    def __init__(self, size=100, content=None):
        self.content = content or []
        self.size = size

    def add(self, item):
        if len(self.content) < self.size:
            self.content.append(item)

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


class Entity:

    def __init__(self, stats):
        self.stats = stats
        self.effects = []

    def receive_damage(self, amount, type):
        amount = self._calculate_damage(amount, type)
        self.remove_stats(Stats({Stat.HP: amount}))
        if self.stats.get(Stat.HP) <= 0:
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


class Player(Entity):

    def __init__(self, stats, inventory):
        super().__init__(stats)
        self.inventory = inventory
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

    def pick_up(self, item):
        self.inventory.add(item)

    def level_up(self):
        pass

    def equip(self, item):
        previous_item = self.item_slots[item.type]
        if previous_item is not None:
            self.remove_stats(previous_item.stats)
            self.inventory.add(previous_item)
        self.add_stats(item.stats)
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
