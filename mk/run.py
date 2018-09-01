from collections import defaultdict
from itertools import count, islice

from .core import Var, walk
from .stream import iterate


def reify(v, s):
    n = defaultdict(count().__next__)

    def _reify(v):
        v = walk(v, s)
        if isinstance(v, Var):
            return "_.{}".format(n[v])
        if isinstance(v, tuple):
            return tuple(map(_reify, v))
        return v

    return _reify(v)


def run(c, v, g):
    for s in islice(iterate(g({})), None if c == 0 else c):
        yield reify(v, s)
