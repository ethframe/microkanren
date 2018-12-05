from collections import defaultdict
from itertools import count, islice

from .stream import unfold
from .unify import Var, Pair, walk, null


class ReifiedVar:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return self.name + ":" + self.type


def reify(v, state):
    subst, types, cons = state
    n = defaultdict(count().__next__)

    def _type(v):
        v = walk(v, types)
        if isinstance(v, Var):
            return "_{}".format(n[v])
        if isinstance(v, Pair):
            v = pairs_as_list(v)
        if isinstance(v, list):
            return "[{}]".format(", ".join(_type(e) for e in v))
        if isinstance(v, tuple):
            return "({})".format(", ".join(_type(e) for e in v))
        return v.__name__

    def _reify(v):
        v = walk(v, subst)
        if isinstance(v, Var):
            return ReifiedVar("_{}".format(n[v]), _type(v))
        if isinstance(v, Pair):
            car = _reify(v.car)
            cdr = _reify(v.cdr)
            if cdr is null:
                return [car]
            if isinstance(cdr, list):
                return [car] + cdr
            return [car, cdr, ...]
        if isinstance(v, list):
            return list(map(_reify, v))
        if isinstance(v, tuple):
            if type(v) == tuple:
                return tuple(map(_reify, v))
            return type(v)._make(map(_reify, v))
        return v

    return _reify(v)


def initial():
    return {}, {}, {}


def run(c, v, g):
    for state in islice(unfold(g(initial())), None if c == 0 else c):
        yield reify(v, state)
