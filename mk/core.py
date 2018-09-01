from .stream import Cons, Empty


class Var:
    pass


def walk(v, s):
    while isinstance(v, Var):
        u = s.get(v)
        if u is None:
            return v
        v = u
    return v


def occurs(v, x):
    if isinstance(x, tuple):
        return any(occurs(v, i) for i in x)
    return v is x


def assign(v, x, s):
    if occurs(v, x):
        return None
    s[v] = x
    return s


def unify(u, v, s):
    u = walk(u, s)
    v = walk(v, s)
    if isinstance(u, Var):
        if isinstance(v, Var) and u is v:
            return s
        return assign(u, v, s)
    elif isinstance(v, Var):
        return assign(v, u, s)
    elif isinstance(u, tuple) and isinstance(v, tuple) and len(u) == len(v):
        for a, b in zip(u, v):
            s = unify(a, b, s)
            if s is None:
                return None
        return s
    return s if u == v else None


def eq(u, v):
    def _goal(s):
        s = unify(u, v, s)
        return Empty() if s is None else Cons(s)
    return _goal


def disj(g1, g2):
    return lambda s: g1(s.copy()).mplus(g2(s))


def conj(g1, g2):
    return lambda s: g1(s).bind(g2)
