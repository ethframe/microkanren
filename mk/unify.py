from collections import namedtuple

from .dispatch import SingledispatchCache


class Var:
    __slots__ = ()


def walk(v, subst):
    while type(v) is Var:
        u = subst.get(v)
        if u is None:
            return v
        v = u
    return v


_occurs_checkers = SingledispatchCache()


def occurs(v, x, subst):
    fn = _occurs_checkers[type(x)]
    if fn:
        return fn(v, x, subst)
    return v is x


def assoc(v, x, subst):
    if occurs(v, x, subst):
        return None
    subst[v] = x
    return [v]


_converters = SingledispatchCache()


def convert(x):
    fn = _converters[type(x)]
    if fn:
        return fn(x)
    return x


def typeof(x):
    if type(x) is Var:
        return x
    return type(convert(x))


_unifiers = SingledispatchCache()


def unify(u, v, subst, list=list):
    u = walk(u, subst)
    v = walk(v, subst)
    if type(u) is Var:
        if u is v:
            return []
        return assoc(u, convert(v), subst)
    if type(v) is Var:
        return assoc(v, convert(u), subst)
    fn = _unifiers[type(u)]
    if fn:
        return fn(u, v, subst)
    if u == v:
        return []


def _tuple_occurs(v, x, subst):
    for e in x:
        if occurs(v, walk(e, subst), subst):
            return True
    return False


def _tuple(u, v, subst):
    if type(u) is type(v) and len(u) == len(v):
        a = []
        for x, y in zip(u, v):
            e = unify(x, y, subst)
            if e is None:
                return None
            a.extend(e)
        return a


_occurs_checkers.add(tuple, _tuple_occurs)
_unifiers.add(tuple, _tuple)


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


_converters.add_exact(list, _convert_list)
_unifiers.add_exact(list, _list)
_unifiers.add_exact(Pair, _pair)
