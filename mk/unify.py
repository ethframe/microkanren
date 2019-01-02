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
