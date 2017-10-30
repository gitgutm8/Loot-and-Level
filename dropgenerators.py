import random
from functools import partial, wraps
from collections import namedtuple


def _fill_up_percentage(func):
    @wraps(func)
    def wrapper(something_to_chance, *args, **kwargs):
        missing_percent = 100 - sum(something_to_chance.values())
        if missing_percent < 0:
            raise ValueError('cannot have more than 100 percent')
        something_to_chance[None] = missing_percent
        return func(something_to_chance, *args, **kwargs)
    return wrapper


@_fill_up_percentage
def ItemDropGenerator(item_prototype_to_chance, num=1):
    item_prototypes, chances = zip(*item_prototype_to_chance.items())
    def generate():
        prototypes = random.choices(item_prototypes, chances, k=num)
        return [p() for p in prototypes if p]
    return generate


GemDropInput = namedtuple('_GemDropInput', ['type', 'rank_to_chance'])


def _get_random_gem_rank(rank_to_chance):
    ranks, chances = zip(*rank_to_chance.items())
    return lambda: random.choices(ranks, chances)[0]


@_fill_up_percentage
def GemDropGenerator(drop_to_chance, num=1):
    gem_drops, chances = zip(*drop_to_chance.items())
    gem_to_rank_randomizer = {
        gem_drop.type: _get_random_gem_rank(gem_drop.rank_to_chance) for gem_drop in gem_drops
    }
    GemTypes = [gem_drop.type for gem_drop in gem_drops]
    def generate():
        GemTypes = random.choices(GemTypes, chances, k=num)
        return [GemType(
            rank=gem_to_rank_randomizer[GemType]()
        ) for GemType in GemTypes if GemType]


def CurrencyDropGenerator(min, max):
    return partial(random.randint, min, max)


def EffectGenerator():
    pass
