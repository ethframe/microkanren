from collections import namedtuple

from mk.run import _reifiers, reify_value
from mk.unify import _converters, _unifiers, convert, unify

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


def _list(u, v, subst):
    if isinstance(v, list):
        v = _convert_list(v)
    elif not (type(v) is Pair or v is null):
        return None
    u = _convert_list(u)
    if u is null:
        if u is v:
            return []
        return None
    return _unify_pairs(u, v, subst)


def _pair(u, v, subst):
    if isinstance(v, list):
        v = _convert_list(v)
    elif not type(v) is Pair:
        return None
    return _unify_pairs(u, v, subst)


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


_converters.add_exact(list, _convert_list)
_unifiers.add_exact(list, _list)
_unifiers.add_exact(Pair, _pair)
_reifiers.add_exact(Pair, _reify_pair)
_reifiers.add_exact(_Null, _reify_null)
