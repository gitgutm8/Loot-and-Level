import pytest
from player import *
from effect import *
from stat import *
from gem import *
from item import *
from blessing import *
from entity import *
from dropgenerators import *
from dataparsing import *


@pytest.fixture
def statless_player():
    return Player(Stats())

@pytest.fixture
def weapon_with_two_sockets():
    return Item(ItemType.WEAPON, '', Stats(), socket_count=2, level=0, rarity=Rarity.COMMON)

@pytest.fixture
def weapon_with_damage():
    return Item(ItemType.WEAPON, '', Stats({Stat.DAMAGE: 100}), 0, 0, Rarity.COMMON)


def test_gem_embedding(statless_player, weapon_with_two_sockets):
    statless_player.pick_up(weapon_with_two_sockets)
    statless_player.equip(weapon_with_two_sockets)
    g1 = DamageGem(GemRank.IMPURE)
    g2 = DamageGem(GemRank.GODLIKE)
    g3 = DamageGem(GemRank.BROKEN)
    for g in [g1, g2, g3]:
        weapon_with_two_sockets.embed_gem(g)
    assert statless_player.stats[Stat.DAMAGE] == 15007, 'embedding gems unsuccessful'
    weapon_with_two_sockets.remove_gem(0)
    assert statless_player.stats[Stat.DAMAGE] == 15000, 'removing gem unsuccessful'
    weapon_with_two_sockets.remove_gem(1)
    assert statless_player.stats[Stat.DAMAGE] == 0, 'removing gem unsuccessful'


@pytest.mark.parametrize(
    'interval,ticks,damage,solution',
    [
        (2, 5, 10, [80, 70, 70, 60, 60, 50, 50, 40, 40] + [30] * 11),
        (1, 10, 4, [76, 72, 68, 64, 60, 56, 52, 48, 44] + [40] * 11)
    ]
)
def test_dot_effect(interval, ticks, damage, solution):
    p = Player(Stats({Stat.MAX_HP: 100, Stat.HP: 80}))
    p.add_effect(DotEffect(
        trigger=BattleTrigger.ROUND_START,
        interval=interval,
        ticks=ticks,
        damage=damage,
        damage_type=DamageType.WATER,
        owner=p
    ))
    #solution = [80, 70, 70, 60, 60, 50, 50, 40, 40] + [30] * 11
    for i in range(20):
        p.on_trigger(BattleTrigger.ROUND_START)
        assert p.stats[Stat.HP] == solution[i], 'damage of dot effect applied incorrectly'


def test_weapon_equipping(statless_player, weapon_with_damage):
    statless_player.pick_up(weapon_with_damage)
    statless_player.equip(weapon_with_damage)
    assert statless_player.stats[Stat.DAMAGE] == weapon_with_damage.stats[Stat.DAMAGE]


@pytest.mark.parametrize(
    'multiplicator', [1.5, 2, 5]
)
def test_blessing(statless_player, weapon_with_damage, multiplicator):
    statless_player.pick_up(weapon_with_damage)
    statless_player.equip(weapon_with_damage)
    b = SingleStatBlessing(Stat.DAMAGE, multiplicator)
    damage_before_blessing = weapon_with_damage.stats[Stat.DAMAGE]
    weapon_with_damage.bless(b)
    assert statless_player.stats[Stat.DAMAGE] == damage_before_blessing * multiplicator, 'blessing does not add damage correctly'
    #g = DamageGem(GemRank.GODLIKE)
    #weapon_with_damage.embed_gem(g)
    #assert statless_player.stats[Stat.DAMAGE] == (100 + 15000) * 1.5, 'blessing + gem working incorrectly'


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
    try:
        print(data.monsters['spider']().drops[1])
    except IndexError:
        print('no drops :(')


if __name__ == '__main__':
    test_data()