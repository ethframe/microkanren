from collections import defaultdict
from itertools import count, islice

from .core import WatchList
from .dispatch import SingledispatchCache
from .stream import unfold
from .unify import Pair, Var, null, walk


class ReifiedVar:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return self.name + ":" + self.type


_reifiers = SingledispatchCache()


def reify_type(v, types, cnt):
    v = walk(v, types)
    if isinstance(v, Var):
        return "_{}".format(cnt[v])
    return v.__name__


def reify_value(v, subst, types, cnt):
    v = walk(v, subst)
    if isinstance(v, Var):
        return ReifiedVar("_{}".format(cnt[v]), reify_type(v, types, cnt))
    fn = _reifiers[type(v)]
    if fn:
        return fn(v, subst, types, cnt)
    return v


def reify(v, state):
    subst, types, cons = state
    cnt = defaultdict(count().__next__)
    return reify_value(v, subst, types, cnt)


def _reify_tuple(v, subst, types, cnt):
    if type(v) == tuple:
        return tuple(reify_value(e, subst, types, cnt) for e in v)
    return type(v)._make(reify_value(e, subst, types, cnt) for e in v)


_reifiers.add(tuple, _reify_tuple)


def _reify_pair(v, subst, types, cnt):
    car = reify_value(v.car, subst, types, cnt)
    cdr = reify_value(v.cdr, subst, types, cnt)
    if cdr is null:
        return [car]
    if isinstance(cdr, list):
        return [car] + cdr
    return [car, cdr, ...]


def _reify_null(v, subst, types, cnt):
    return []


_reifiers.add_exact(Pair, _reify_pair)
_reifiers.add_exact(type(null), _reify_null)


def initial():
    return {}, {}, WatchList()


def run(c, v, g):
    for state in islice(unfold(g(initial())), None if c == 0 else c):
        yield reify(v, state)
