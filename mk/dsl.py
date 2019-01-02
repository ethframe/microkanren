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


def zzz(thunk):
    return lambda state: Thunk(lambda: thunk()(state))


def delay(fn):
    @wraps(fn)
    def _constructor(*args):
        return lambda state: Thunk(lambda: fn(*args)(state))
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