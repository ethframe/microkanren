from collections import namedtuple


class Var:
    pass


null = object()
Pair = namedtuple("Pair", "car cdr")


def walk(v, subst):
    while isinstance(v, Var):
        u = subst.get(v)
        if u is None:
            break
        v = u
    return v


def occurs(v, x, subst):
    if isinstance(x, tuple):
        return any(occurs(v, walk(e, subst), subst) for e in x)
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
    if isinstance(u, list):
        u = list_as_pairs(u)
    if isinstance(v, list):
        v = list_as_pairs(v)
    if isinstance(u, Var):
        return [] if u is v else assoc(u, v, subst)
    if isinstance(v, Var):
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
    return [] if u == v else None
