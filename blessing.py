from stats import Stats, Stat


class Blessing:

    def __init__(self, stats):
        self.stats = stats

    def add(self, item):
        item.add_stats(self.stats)

    def remove(self):
        item.remove_stats(self.stats)


def SingleStatBlessing(stat, multiplicator):
    return Blessing(
        Stats({stat: (0, multiplicator)})
    )
