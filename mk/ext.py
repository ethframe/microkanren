import inspect
from functools import reduce, wraps

from .core import copy
from .run import run
from .stream import Thunk
from .unify import Var, walk


def call_fresh(fn):
    return lambda s: fn(Var())(s)


def conjp(g, *gs):
    return lambda state: reduce(lambda s, g: s.bind(g), gs, g(state))


def disjp(g, *gs):
    return lambda state: reduce(
        lambda s, o: s.mplus(o), [g(copy(state)) for g in gs], g(state)
    )


def conde(*ggs):
    return disjp(*(conjp(*gs) for gs in ggs))


def fresh(fn):
    sig = inspect.signature(fn)
    if not all(
        p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
        for p in sig.parameters.values()
    ):
        raise ValueError(fn)
    n = len(sig.parameters)
    return lambda s: fn(*(Var() for _ in range(n)))(s)


def zzz(thunk):
    return lambda state: Thunk(lambda: thunk()(state))


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
