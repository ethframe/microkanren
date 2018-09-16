class Var:
    pass


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


def unify(u, v, subst):
    u = walk(u, subst)
    v = walk(v, subst)
    if isinstance(u, Var):
        return [] if u is v else assoc(u, v, subst)
    elif isinstance(v, Var):
        return assoc(v, u, subst)
    elif isinstance(u, tuple) and isinstance(v, tuple) and len(u) == len(v):
        if type(u) != type(v):
            return None
        a = []
        for x, y in zip(u, v):
            e = unify(x, y, subst)
            if e is None:
                return None
            a.extend(e)
        return a
    return [] if u == v else None
