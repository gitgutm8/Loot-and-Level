from player import *
from effect import *
from stat import *
from gem import *
from item import *
from blessing import *
from entity import *
from dropgenerators import *
from dataparsing import *


def test_gem_embedding():
    p = Player(Stats({Stat.MAX_HP: 100, Stat.HP: 80}))
    i = Item(ItemType.WEAPON, '', Stats(), socket_count=2, level=0, rarity=Rarity.COMMON)
    p.pick_up(i)
    p.equip(i)
    g1 = DamageGem(GemRank.IMPURE)
    g2 = DamageGem(GemRank.GODLIKE)
    g3 = DamageGem(GemRank.BROKEN)
    for g in [g1, g2, g3]:
        i.embed_gem(g)
    assert p.stats[Stat.DAMAGE] == 15007, 'embedding gems unsuccessful'
    i.remove_gem(0)
    assert p.stats[Stat.DAMAGE] == 15000, 'removing gem unsuccessful'
    i.remove_gem(1)
    assert p.stats[Stat.DAMAGE] == 0, 'removing gem unsuccessful'


def test_dot_effect():
    p = Player(Stats({Stat.MAX_HP: 100, Stat.HP: 80}))
    p.add_effect(DotEffect(
        trigger=BattleTrigger.ROUND_START,
        interval=2,
        ticks=5,
        damage=10,
        damage_type=DamageType.WATER,
        owner=p
    ))
    solution = [80, 70, 70, 60, 60, 50, 50, 40, 40] + [30] * 11
    for i in range(20):
        p.on_trigger(BattleTrigger.ROUND_START)
        assert p.stats[Stat.HP] == solution[i], 'damage of dot effect applied incorrectly'


def test_poison_gem():
    p = Player(Stats({Stat.MAX_HP: 100, Stat.HP: 80}))
    p.enemy = Entity(Stats({Stat.HP: 100}))
    i = Item(ItemType.NECKLACE, '[name]', Stats(), 1, 90, Rarity.EPIC)
    p.pick_up(i)
    p.equip(i)
    g = PoisonGem(GemRank.IMPURE)
    i.embed_gem(g)


def test_blessing():
    p = Player(Stats())
    i = Item(ItemType.WEAPON, '', Stats({Stat.DAMAGE: 100}), 1, 1, Rarity.LEGENDARY)
    p.pick_up(i)
    p.equip(i)
    assert p.stats[Stat.DAMAGE] == 100, 'equipping weapon does not add damage'
    b = SingleStatBlessing(Stat.DAMAGE, 1.5)
    i.bless(b)
    assert p.stats[Stat.DAMAGE] == 150, 'blessing does not add damage correctly'
    g = DamageGem(GemRank.GODLIKE)
    i.embed_gem(g)
    assert p.stats[Stat.DAMAGE] == (100 + 15000) * 1.5, 'blessing + gem working incorrectly'


def test_gem_combining():
    g1, g2, g3 = DamageGem(GemRank.BROKEN), DamageGem(GemRank.BROKEN), DamageGem(GemRank.BROKEN)
    p = Player(Stats())
    p.pick_up(g1)
    p.pick_up(g2)
    p.pick_up(g3)
    p.combine_gems(g1, g2, g3)
    assert g1.rank == GemRank.IMPURE, 'combining does not increase rank'
    assert p.inventory.content == [g1], 'combining does not remove gems from inventory'


def test_item_drop_generator():
    p = Player(Stats())
    dg = ItemDropGenerator(
        {
            ItemPrototype(
                ItemType.WEAPON, 'Schwert der Schwere', Rarity.EPIC,
                Stats({Stat.DAMAGE: 25}), Stats({Stat.DAMAGE: 32}),
                min_sockets=2, max_sockets=3,
                min_level=40, max_level=45
            ) : 50,
        }
    )
    for _ in range(10):
        i = dg()
        if i:
            print(vars(i[0]))


def test_data():
    import json
    with open('item_data.json') as idata, open('monster_data.json', 'rt') as mdata:
        item_data = json.load(idata)
        monster_data = json.load(mdata)
    data = JsonDataParser(item_data, monster_data)
    for d in data:
        print(d())


test_gem_embedding()
test_dot_effect()
test_poison_gem()
test_blessing()
test_gem_combining()
#test_item_drop_generator()
test_data()

print('all tests successful')
