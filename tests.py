from Player import *
from Effects import *
from Stats import *
from Gems import *
from Items import *


def test_gem_embedding():
    p = Player(Stats({Stat.MAX_HP: 100, Stat.HP: 80}), Inventory())
    i = Item(ItemType.WEAPON, '', p, Stats(), socket_count=2, level=0, rarity=Rarity.COMMON)
    p.pick_up(i)
    p.equip(i)
    g1 = DamageGem(GemRank.IMPURE, p)
    g2 = DamageGem(GemRank.GODLIKE, p)
    g3 = DamageGem(GemRank.BROKEN, p)
    for g in [g1, g2, g3]:
        i.embed_gem(g)
    assert p.stats[Stat.DAMAGE] == 15007, 'embedding gems unsucessful'
    i.remove_gem(0)
    assert p.stats[Stat.DAMAGE] == 15000, 'removing gem unsucessful'


def test_dot_effect():
    p = Player(Stats({Stat.MAX_HP: 100, Stat.HP: 80}), Inventory())
    p.add_effect(DotEffect(
        trigger=Trigger.ROUND_START,
        interval=2,
        total_ticks=5,
        damage=10,
        damage_type=DamageType.WATER,
        owner=p
    ))

    solution = [80, 70, 70, 60, 60, 50, 50, 40, 40] + [30] * 11
    for i in range(20):
        p.on_trigger(Trigger.ROUND_START)
        assert p.stats.get(Stat.HP) == solution[i], 'error in `test_dot_effect'


def test_poison_gem():
    p = Player(Stats({Stat.MAX_HP: 100, Stat.HP: 80}), Inventory())
    p.enemy = Entity(Stats({Stat.HP: 100}))
    i = Item(ItemType.NECKLACE, 'LUL', p, Stats(), 1, 90, Rarity.EPIC)
    p.pick_up(i)
    p.equip(i)
    g = PoisonGem(GemRank.IMPURE, p)
    i.embed_gem(g)


test_gem_embedding()
test_dot_effect()
test_poison_gem()
