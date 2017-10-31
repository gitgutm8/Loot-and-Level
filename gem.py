import random
from enum import Enum, auto
from stats import *
from battle import BattleTrigger
from effect import *


class GemRank(Enum):
    BROKEN = auto()
    IMPURE = auto()
    SIMPLE = auto()
    POLISHED = auto()
    RADIANT = auto()
    PERFECT = auto()
    ROYAL = auto()
    HOLY = auto()
    GODLIKE = auto()

NEXT_RANK = {rank: next_rank for rank, next_rank in zip(GemRank, list(GemRank)[1:])}


class Gem:

    RANK_TO_EFFECT = [{}] * len(GemRank)

    RANK_TO_NAME = {
        GemRank.BROKEN  : 'Zerbrochener',
        GemRank.IMPURE  : 'Unreiner',
        GemRank.SIMPLE  : 'Einfacher',
        GemRank.POLISHED: 'Geschliffener',
        GemRank.RADIANT : 'Strahlender',
        GemRank.PERFECT : 'Perfekter',
        GemRank.ROYAL   : 'Königlicher',
        GemRank.HOLY    : 'Heiliger',
        GemRank.GODLIKE : 'Göttlicher'
    }

    def __init__(self, rank):
        self.rank = rank
        self.name = self.RANK_TO_NAME[rank] + ' ' + self.type_name
        self.stats = self.RANK_TO_EFFECT[rank]

    def rank_up(self):
        self.rank = NEXT_RANK[self.rank]

    def get_picked_up(self, by):
        pass

    def on_embedding(self, item):
        pass

    def on_removal(self, item):
        pass


class StatGemMeta(type):

    def __init__(cls, *args):
        if len(cls.RANK_TO_EFFECT) != len(GemRank):
            raise ValueError(
                f'invalid amount of gemranks in {cls}:'
                f'expected {len(GemRank)}, got {len(cls.RANK_TO_EFFECT)}'
            )
        cls.RANK_TO_EFFECT = {
            rank: Stats(stats)
            for rank, stats
            in zip(GemRank, cls.RANK_TO_EFFECT)
        }


class StatGem(Gem, metaclass=StatGemMeta):

    def on_embedding(self, item):
        item.add_stats(self.stats)

    def on_removal(self, item):
        item.remove_stats(self.stats)

    def __str__(self):
        return f'{self.name}:\n{self.stats}'


class DamageGem(StatGem):

    type_name = 'Rubin'

    RANK_TO_EFFECT = [
        {Stat.DAMAGE: 3},
        {Stat.DAMAGE: 7},
        {Stat.DAMAGE: 19},
        {Stat.DAMAGE: 55},
        {Stat.DAMAGE: 160},
        {Stat.DAMAGE: 470},
        {Stat.DAMAGE: 1400},
        {Stat.DAMAGE: 4200},
        {Stat.DAMAGE: 15000},
    ]


class HPGem(StatGem):

    type_name = 'Smaragd'

    RANK_TO_EFFECT = [
        {Stat.HP: 30},
        {Stat.HP: 65},
        {Stat.HP: 172},
        {Stat.HP: 400},
        {Stat.HP: 1111},
        {Stat.HP: 3210},
        {Stat.HP: 8600},
        {Stat.HP: 25000},
        {Stat.HP: 75000},
    ]


def __comment():
    # lol
    class ArmorGem(StatGem):

        type_name = 'Azurit'

        RANK_TO_EFFECT = []


    class ResistanceGem(StatGem):

        type_name = 'Amethyst'

        RANK_TO_EFFECT = []


    class CritchanceGem(StatGem):

        type_name = 'Citrin'

        RANK_TO_EFFECT = []


    class CritdamageGem(StatGem):

        type_name = 'Bernstein'

        RANK_TO_EFFECT = []


class EffectApplyingGemMeta(type):

    def __init__(cls, *args):
        if len(cls.RANK_TO_EFFECT) != len(GemRank):
            raise ValueError(
                f'invalid amount of gemranks in {cls}:'
                f'expected {len(GemRank)}, got {len(cls.RANK_TO_EFFECT)}'
            )
        cls.RANK_TO_EFFECT = {
            rank: effect
            for rank, effect
            in zip(GemRank, cls.RANK_TO_EFFECT)
        }


class EffectApplyingGem(Gem, metaclass=EffectApplyingGemMeta):

    def on_embedding(self, item):
        self.effect = self.create_effect(item)
        item.owner.add_effect(self.effect)

    def on_removal(self, item):
        item.owner.remove_effect(self.effect)


class EnemyAffectingGem(EffectApplyingGem):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wrapper = self._create_battle_wrapper()

    def on_embedding(self, item):
        item.owner.add_battle_wrapper(self.wrapper)

    def on_removal(self, item):
        item.owner.remove_battle_wrapper(self.wrapper)


class ReflectDamageGem(EnemyAffectingGem):

    type_name = 'Obsidian'

    RANK_TO_EFFECT = [
        {'percentage': 3},
        {'percentage': 5},
        {'percentage': 8},
        {'percentage': 11},
        {'percentage': 15},
        {'percentage': 19},
        {'percentage': 24},
        {'percentage': 29},
        {'percentage': 35},
    ]

    def _create_battle_wrapper(self):
        class Wrapper:

            def prepare(wrapper, owner):
                wrapper.effect = ParametrizedDamageEffect(
                    trigger=BattleTrigger.HIT_BY_ENEMY,
                    target=owner.current_battle.enemy_of(owner),
                    damage=0,
                    damage_type=0,
                    calculator=self._damage_calculator(owner.current_battle)
                )
                owner.add_effect(wrapper.effect)

            def cleanup(wrapper, owner):
                owner.remove_effect(wrapper.effect)

        return Wrapper()

    def _damage_calculator(self, battle):
        def inner(damage_effect):
            attack = battle.last_action()
            damage_effect.damage = attack['damage_dealt'] / 100 * self.stats['percentage']
            damage_effect.damage_type = attack['dtype']
        return inner



class PoisonGem(EnemyAffectingGem):

    type_name = 'Peridot'

    RANK_TO_EFFECT = [
        {'damage_per_tick': 2, 'total_ticks': 2},
        {'damage_per_tick': 3, 'total_ticks': 3},
        {'damage_per_tick': 5, 'total_ticks': 3},
        {'damage_per_tick': 9, 'total_ticks': 4},
        {'damage_per_tick': 20, 'total_ticks': 5},
        {'damage_per_tick': 55, 'total_ticks': 5},
        {'damage_per_tick': 160, 'total_ticks': 5},
        {'damage_per_tick': 480, 'total_ticks': 6},
        {'damage_per_tick': 1500, 'total_ticks': 7}
    ]

    def _create_battle_wrapper(self):
        class Wrapper:

            def prepare(wrapper, owner):
                wrapper.effect = RandomEffect(
                    # TODO: Put in real value
                    chance=30,
                    trigger=BattleTrigger.HIT,
                    target=owner.current_battle.enemy_of(owner),
                    EffectType=EffectAddingEffect,
                    effect_to_add={
                        'type': DotEffect,
                        'trigger': BattleTrigger.ROUND_START,
                        'damage': self.stats['damage_per_tick'],
                        'damage_type': DamageType.TRUE_DAMAGE,
                        'interval': 1,
                        'total_ticks': self.stats['total_ticks']
                    }
                )
                owner.add_effect(wrapper.effect)

            def cleanup(self, owner):
                owner.remove_effect(self.effect)

        return Wrapper()


if __name__ == '__main__':
    #print(DamageGem.RANK_TO_STATS)
    print(DamageGem(GemRank.GODLIKE, 0))