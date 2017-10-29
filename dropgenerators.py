import random
from functools import partial
from collections import namedtuple


def _cumulate_weights(percentages):
    weights = [percentages[0] / 100]
    for percentage in percentages:
        weights.append(percentage / 100 + weights[-1])
    return weights


def ItemDropGenerator(item_prototype_to_chance):
    item_prototypes, chances = zip(*item_prototype_to_chance.items())
    cum_weights = _cumulate_weights(chances)
    def generate():
        prototype = random.choices(item_prototypes, cum_weights=cum_weights)
        return prototype()
    return generate


GemDropInput = namedtuple('_GemDropInput', ['type', 'rank_to_chance'])


def _get_random_gem_rank(rank_to_chance):
    ranks, chances = zip(*rank_to_chance.items())
    cum_weights = _cumulate_weights(chances)
    return partial(random.choices, ranks, cum_weights=cum_weights)


def GemDropGenerator(drop_to_chance):
    gem_drops, chances = zip(*drop_to_chance.items())
    cum_weights = _cumulate_weights(chances)
    gem_to_rank_randomizer = {
        gem_drop.type: _get_random_gem_rank(gem_drop.rank_to_chance) for gem_drop in gem_drops
    }
    GemTypes = [gem_drop.type for gem_drop in gem_drops]
    def generate():
        GemType = random.choices(GemTypes, cum_weights=cum_weights)
        return GemType(
            rank=gem_to_rank_randomizer[GemType]()
        )



def EffectGenerator():
    pass