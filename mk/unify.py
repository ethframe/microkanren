from collections import namedtuple


class Var:
    __slots__ = ()


null = object()
Pair = namedtuple("Pair", "car cdr")


def walk(v, subst):
    while type(v) is Var:
        u = subst.get(v)
        if u is None:
            return v
        v = u
    return v


def occurs(v, x, subst):
    if isinstance(x, tuple):
        for e in x:
            if occurs(v, walk(e, subst), subst):
                return True
        return False
    return v is x


def assoc(v, x, subst):
    if occurs(v, x, subst):
        return None
    subst[v] = x
    return [v]


def list_as_pairs(x):
    if len(x) >= 2 and x[-1] is Ellipsis:
        p = x[-2]
        x = x[:-2]
    else:
        p = null
    for e in reversed(x):
        p = Pair(e, p)
    return p


def pairs_as_list(p):
    x = []
    while isinstance(p, Pair):
        x.append(p.car)
        p = p.cdr
    if p is not null:
        x.append(Ellipsis)
    return x


def unify(u, v, subst, list=list):
    u = walk(u, subst)
    v = walk(v, subst)
    if type(v) is list:
        v = list_as_pairs(v)
    if type(u) is Var:
        if u is v:
            return []
        return assoc(u, v, subst)
    if type(u) is list:
        u = list_as_pairs(u)
    if type(v) is Var:
        return assoc(v, u, subst)
    if isinstance(u, tuple) and isinstance(v, tuple) and len(u) == len(v):
        if type(u) is not type(v):
            return None
        a = []
        for x, y in zip(u, v):
            e = unify(x, y, subst)
            if e is None:
                return None
            a.extend(e)
        return a
    if u == v:
        return []
    return None
