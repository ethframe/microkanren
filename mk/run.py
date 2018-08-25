from collections import defaultdict
from itertools import count, islice


from .core import Var, walk, is_pair, unwrap


def _reify(v, s, n):
    v = walk(v, s)
    if isinstance(v, Var):
        return n[v]
    if is_pair(v):
        return (_reify(v[0], s, n), _reify(v[1], s, n))
    return v


def reify(v, s):
    c = count().__next__
    n = defaultdict(lambda: "_{}".format(c()))
    return _reify(v, s, n)


def run(c, v, g):
    if c == 0:
        c = None
    for s in islice(unwrap(g({})), c):
        yield reify(v, s)
