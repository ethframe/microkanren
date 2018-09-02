import inspect

from .core import Var, conj, disj
from .run import run
from .stream import Thunk


def call_fresh(fn):
    return lambda s: fn(Var())(s)


def conjp(g, *gs):
    if gs:
        return conj(g, conjp(*gs))
    return g


def disjp(g, *gs):
    if gs:
        return disj(g, disjp(*gs))
    return g


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


def zzz(fn):
    return lambda s: Thunk(lambda: fn()(s))


def runp(c, v, *gs):
    return run(c, v, conjp(*gs))