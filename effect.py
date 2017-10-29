import random
import inspect
from copy import deepcopy


class _Effect:
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


class _DamagingEffect(_Effect):

    def __init__(self, damage, damage_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.damage = damage
        self.damage_type = damage_type

    def apply(self):
        self.target.receive_damage(self.damage, self.damage_type)


class _HealingEffect(_Effect):

    def __init__(self, *args, heal_amount, **kwargs):
        super().__init__(*args, **kwargs)
        self.heal_amount = heal_amount

    def apply(self):
        self.target.heal(self.heal_amount)


class EffectAddingEffect(_Effect):

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
        self.EffectType = effect_to_add.pop('type')
        self.effect_to_add = effect_to_add

    def apply(self):
        eff = self.EffectType(**self.effect_to_add, owner=self.target)
        self.target.add_effect(eff)


class ConditionalEffect:

    def __init__(self, *args, condition, **kwargs):
        super().__init__(*args, **kwargs)
        sig = inspect.signature(condition)
        # Can't have a condition function with no arguments
        if (len(sig.parameters)) == 0:
            condition = lambda _: condition()
        self.condition = condition

    def apply(self):
        if self.condition(self):
            super().apply()


class TimedEffect:

    def __init__(self, *args, times, **kwargs):
        super().__init__(*args, **kwargs)
        self.times = times

    def apply(self):
        self.times -= 1
        if self.times < 0:
            self.remove()
        else:
            super().apply()


class DelayedEffect:

    def __init__(self, *args, delay, **kwargs):
        super().__init__(*args, **kwargs)
        self.delay = delay
        self.timer = delay

    def apply(self):
        self.timer -= 1
        if not self.timer:
            self.timer = self.delay
            super().apply()


class ConditionalEffectAdder(ConditionalEffect, EffectAddingEffect):
    pass


def build_effect(*effects, **attrs):
    CustomEffect = type('', effects, {})
    return CustomEffect(**attrs)


def DotEffect(ticks, interval, **kwargs):
    return build_effect(
        DelayedEffect, TimedEffect, _DamagingEffect,
        times=ticks, delay=interval, **kwargs
    )


def RandomEffect(EffectType, chance, *args, **kwargs):
    MyRandomEffect = type('', (ConditionalEffect, EffectType), {})
    return MyRandomEffect(
        *args,
        condition=lambda: random.uniform(0, 100) < chance,
        **kwargs
    )