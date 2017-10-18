from enum import Enum, auto


class BattleActions(Enum):
    DAMAGE_DEALT = auto()
    HEAL = auto()
    BUFF = auto()
    DEBUFF = auto()


class Battle:

    def __init__(self, *teams):
        self.teams = teams
        self.current_round = 0
        self.log = []

    def play_round(self):
        self.current_round += 1

    def last_action(self):
        return self.log[-1]



class Attack:

    def __init__(
        self, damage, damage_type,
        crit_chance, crit_multiplier,
        attacker, attacked
    ):
        self.damage = damage
        self.damage_type = damage_type
        self.crit_chance = crit_chance
        self.crit_multiplier = crit_multiplier
        self.attacker = attacker
        self.attacked = attacked
