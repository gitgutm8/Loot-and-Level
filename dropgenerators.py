import random
from functools import partial
from collections import namedtuple


def _fill_up_percentage(something_to_chances):
    missing_percent = 100 - sum(something_to_chances.values())
    if missing_percent < 0:
        raise ValueError('cannot have more than 100 percent')
    something_to_chances[None] = missing_percent


def ItemDropGenerator(item_prototype_to_chance, num=1):
    """
    Returns a callable that generates items using the given prototypes and chances.
    Chances do not have to add up to (but must not exceed) 100.

    :param item_prototype_to_chance: Mapping from item prototype to its chance to drop.
    :param num: maximum number of items that may drop.
    :return: callable generating items
    """
    _fill_up_percentage(item_prototype_to_chance)
    item_prototypes, chances = zip(*item_prototype_to_chance.items())
    def generate_item():
        prototypes = random.choices(item_prototypes, chances, k=num)
        return [p() for p in prototypes if p]
    return generate_item


def _get_random_gem_rank(rank_to_chance):
    ranks, chances = zip(*rank_to_chance.items())
    return lambda: random.choices(ranks, chances)[0]


def GemDropGenerator(
    gem_to_chance: dict,
    ranks_to_chances: list,
    num=1
):
    _fill_up_percentage(gem_to_chance)
    gem_types, chances = zip(*gem_to_chance.items())
    type_to_rank_randomizer = {
        GemType: _get_random_gem_rank(rank_to_chance)
        for GemType, rank_to_chance
        in zip(gem_types, ranks_to_chances)
    }
    def generate_gem():
        chosen_gem_types = random.choices(gem_types, chances, k=num)
        return [GemType(
            rank=type_to_rank_randomizer[GemType]()
        ) for GemType in chosen_gem_types if GemType]
    return generate_gem


def CurrencyDropGenerator(Currency, min, max):
    def generate_currency():
        return Currency(random.randint(min, max))
    return generate_currency


def EffectGenerator():
    pass
