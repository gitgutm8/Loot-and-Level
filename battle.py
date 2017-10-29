from enum import Enum, auto


class BattleActions(Enum):
    DAMAGE_DEALT = auto()
    HEAL = auto()
    BUFF = auto()
    DEBUFF = auto()


class Battle:

    def __init__(self, enemy):
        self.enemy = enemy
        self.current_round = 0
        self.log = []

    def play_round(self):
        self.current_round += 1

    def last_action(self):
        return self.log[-1]
