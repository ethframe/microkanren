from collections import namedtuple

from mk.registry import register_exact
from mk.run import reify_value
from mk.stream import MZero, Unit
from mk.unify import Var, convert, unify, walk

Pair = namedtuple("Pair", "car, cdr")


class _Null:
    __slots__ = ()


null = _Null()


def _convert_list(x):
    if len(x) >= 2 and x[-1] is Ellipsis:
        p = convert(x[-2])
        x = x[:-2]
    else:
        p = null
    for e in reversed(x):
        p = Pair(convert(e), p)
    return p


def _unify_pairs(u, v, subst):
    a = []
    while type(u) is Pair and type(v) is Pair:
        e = unify(u.car, v.car, subst)
        if e is None:
            return None
        a.extend(e)
        u, v = u.cdr, v.cdr
    e = unify(u, v, subst)
    if e is not None:
        a.extend(e)
        return a


def _null(u, v, subst):
    if v is not null:
        return None
    return []


def _pair(u, v, subst):
    if type(v) is not Pair:
        return None
    return _unify_pairs(u, v, subst)


def _reify_pair(v, subst, types, cnt):
    car = reify_value(v.car, subst, types, cnt)
    cdr = reify_value(v.cdr, subst, types, cnt)
    if isinstance(cdr, list):
        return [car] + cdr
    return [car, cdr, ...]


def _reify_null(v, subst, types, cnt):
    return []


register_exact(list, convert=_convert_list)
register_exact(Pair, unify=_pair, reify=_reify_pair)
register_exact(_Null, unify=_null, reify=_reify_null)


def no_item(val, pred):
    val = convert(val)

    def _goal(state):
        a = walk(val, state[0])
        if type(a) is Var:
            cons = state[2]
            cons[a].append(_goal)
            return Unit(state)
        if type(a) is Pair:
            return Unit(state).\
                bind(no_item(a.car, pred)).\
                bind(no_item(a.cdr, pred))
        if pred(a):
            return MZero()
        return Unit(state)
    return _goal
