class Var:
    __slots__ = ("value", "scope")

    def __init__(self, scope=None):
        self.value = None
        self.scope = scope


def is_pair(x):
    return isinstance(x, tuple) and len(x) == 2


def walk(v, s):
    while isinstance(v, Var):
        if v.value is None:
            u = s.get(v)
            if u is None:
                return v
            v = u
        else:
            v = v.value
    return v


def occurs(v, x):
    if is_pair(x):
        return occurs(v, x[0]) or occurs(v, x[1])
    return v is x


def assign(v, x, s):
    if occurs(v, x):
        return None
    if s is v.scope:
        v.value = x
    else:
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
    elif is_pair(u) and is_pair(v):
        return None if unify(u[0], v[0], s) is None else unify(u[1], v[1], s)
    return s if u == v else None


def eq(u, v):
    def _goal(s):
        s = unify(u, v, s)
        if s is not None:
            return (s, None)
    return _goal


def mplus(s1, s2):
    if s1 is None:
        return s2
    if callable(s1):
        return lambda: mplus(s2, s1())
    return (s1[0], mplus(s1[1], s2))


def bind(s, g):
    if s is None:
        return None
    if callable(s):
        return lambda: bind(s(), g)
    return mplus(g(s[0]), bind(s[1], g))


def disj(g1, g2):
    return lambda s: mplus(g1(s.copy()), g2(s.copy()))


def conj(g1, g2):
    return lambda s: bind(g1(s), g2)


def unwrap(s):
    while s is not None:
        if callable(s):
            s = s()
        else:
            i, s = s
            yield i
