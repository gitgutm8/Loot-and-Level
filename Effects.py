import random
from copy import deepcopy


class Effect:
    """Everything that can change something while battling."""

    def __init__(self, trigger, owner, self_targetting=True):
        self.trigger = trigger
        self.owner = owner
        self.self_targetting = self_targetting

    @property
    def target(self):
        if self.self_targetting:
            return self.owner
        return self.owner.get_enemy()

    def apply(self):
        pass

    def remove(self):
        self.owner.remove_effect(self)


class ConditionalEffectMixin:

    def __init__(self, *args, condition, **kwargs):
        super().__init__(*args, **kwargs)
        self.condition = condition

    def apply(self):
        if self.condition():
            super().apply()


def create_random_effect(effect_type, chance, *args, **kwargs):
    RandomEffect = type('', (ConditionalEffectMixin, effect_type), {})
    return RandomEffect(
        *args,
        condition=lambda: random.uniform(0, 100) < chance,
        **kwargs
    )


class EffectAddingEffect(Effect):

    def __init__(self, effect_to_add, *args, **kwargs):
        """
        :param dict effect_to_add:
            A mapping having the following structure:
                {
                'type': class of effect to create,
                other key-value pairs representing the
                attributes the new effect needs, except
                for `owner`
                }
        """
        super().__init__(*args, **kwargs)
        self.effect_type = effect_to_add.pop('type')
        self.effect_to_add = effect_to_add

    def apply(self):
        eff = self.effect_type(**self.effect_to_add, owner=self.target)
        self.target.add_effect(eff)
        #self.remove()


class ConditionalEffectAdder(ConditionalEffectMixin, EffectAddingEffect):
    pass


class _DamagingEffect(Effect):

    def __init__(self, damage, damage_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.damage = damage
        self.damage_type = damage_type

    def apply(self):
        self.target.receive_damage(self.damage, self.damage_type)


class DelayedDamage(_DamagingEffect):

    def __init__(self, delay, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delay = delay

    def apply(self):
        self.delay -= 1
        if self.delay <= 0:
            super().apply()
            self.remove()


class DotEffect(_DamagingEffect):

    def __init__(self, total_ticks, interval, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_ticks = total_ticks
        self.interval = interval
        self.counter = 0

    def apply(self):
        self.counter = (self.counter+1) % self.interval
        if not self.counter:
            super().apply()
            self.total_ticks -= 1
            if self.total_ticks <= 0:
                self.remove()
