from enum import Enum, auto
import random
from itertools import chain
from stats import Stat, DamageType


class BattleTrigger(Enum):
    HIT = auto()
    ROUND_START = auto()
    ENEMY_ROUND_START = auto()
    BATTLE_START = auto()
    HIT_BY_ENEMY = auto()
    BATTLE_END = auto()
    BATTLE_WON = auto()
    BATTLE_LOST = auto()


class BattleAction(Enum):
    DAMAGE_DEALT = auto()
    HEAL = auto()
    BUFF = auto()
    DEBUFF = auto()


class Battle:

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.current_round = 0
        self.log = []

    def enemy_of(self, who):
        return {self.enemy: self.player, self.player: self.enemy}[who]

    def fight(self):
        self._begin()
        while self.player.alive() and self.enemy.alive():
            self._play_round()
        self._end()

    def _begin(self):
        self.player.current_battle = self.enemy.current_battle = self
        self.player.prepare_battle_wrappers()
        self.enemy.prepare_battle_wrappers()
        self._broadcast(BattleTrigger.BATTLE_START)

    def _end(self):
        self._broadcast(BattleTrigger.BATTLE_END)
        if self.player.alive():
            self.player.on_trigger(BattleTrigger.BATTLE_WON)
            self.enemy.on_trigger(BattleTrigger.BATTLE_LOST)
        else:
            self.player.on_trigger(BattleTrigger.BATTLE_LOST)
            self.enemy.on_trigger(BattleTrigger.BATTLE_WON)

        self.player.cleanup_battle_wrappers()
        self.enemy.cleanup_battle_wrappers()
        self.player.current_battle = self.enemy.current_battle = None

    def _play_round(self):
        self.current_round += 1
        for fighter, other in [(self.player, self.enemy), (self.enemy, self.player)]:
            fighter.on_trigger(BattleTrigger.ROUND_START)
            other.on_trigger(BattleTrigger.ENEMY_ROUND_START)
            self._calculate_damage(fighter, other)
            fighter.on_trigger(BattleTrigger.HIT)
            other.on_trigger(BattleTrigger.HIT_BY_ENEMY)

    def last_action(self):
        return self.log[-1]

    def _calculate_damage(self, fighter, other):
        does_crit = fighter.stats[Stat.CRIT_CHANCE] < random.uniform(0, 100)
        damage = fighter.stats[Stat.DAMAGE] * (1 + fighter.stats[Stat.CRIT_BONUS] * does_crit)
        damage_dealt = other.receive_damage(damage, DamageType.NORMAL)
        self.log.append({
            'type': BattleAction.DAMAGE_DEALT,
            'damage_dealt': damage_dealt,
            'dtype': DamageType.NORMAL,
            'attacker': fighter,
            'attacked': other
        })

    def _broadcast(self, trigger):
        self.player.on_trigger(trigger)
        self.enemy.on_trigger(trigger)
