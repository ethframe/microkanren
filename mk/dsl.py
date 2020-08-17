from functools import reduce, wraps

from .core import copy
from .run import run
from .stream import Thunk
from .unify import Var, walk


def fresh(fst, *args):
    if not args:
        return fst(Var())
    (fn,) = args
    return fn(*(Var() for _ in range(fst)))


def conjp(g, *gs):
    return lambda state: reduce(
        lambda s, g: s.bind(g), gs, g(state)
    )


def disjp(g, *gs):
    return lambda state: reduce(
        lambda s, o: s.mplus(o), [g(copy(state)) for g in gs], g(state)
    )


def conde(*ggs):
    return disjp(*(gs if callable(gs) else conjp(*gs) for gs in ggs))


class Zzz:
    __slots__ = ('fn', 'state')

    def __init__(self, fn, state):
        self.fn = fn
        self.state = state

    def __call__(self):
        return self.fn()(self.state)


def zzz(thunk):
    return lambda state: Thunk(Zzz(thunk, state))


class Delay:
    __slots__ = ('fn', 'args', 'state')

    def __init__(self, fn, args, state):
        self.fn = fn
        self.args = args
        self.state = state

    def __call__(self):
        return self.fn(*self.args)(self.state)


def delay(fn):
    @wraps(fn)
    def _constructor(*args):
        return lambda state: Thunk(Delay(fn, args, state))
    return _constructor


def runp(c, v, *gs):
    return run(c, v, conjp(*gs))


def walk_args(fn):
    @wraps(fn)
    def _constructor(*args):
        def _goal(state):
            subst = state[0]
            return fn(_goal, state, *(walk(a, subst) for a in args))
        return _goal
    return _constructor
