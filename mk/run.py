from collections import defaultdict
from itertools import count, islice

from .core import initial
from .dispatch import SingledispatchCache
from .stream import unfold
from .unify import Var, walk


class ReifiedVar:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return self.name + ":" + self.type


_reifiers = SingledispatchCache()


def reify_type(v, types, cnt):
    t_v = types.get(v)
    if t_v is None:
        return "_{}".format(cnt[v])
    return t_v.__name__


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


def run(c, v, g):
    for state in islice(unfold(g(initial())), None if c == 0 else c):
        yield reify(v, state)
