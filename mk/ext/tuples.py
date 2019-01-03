from mk.registry import register
from mk.run import reify_value
from mk.unify import occurs, unify, walk


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


def _reify_tuple(v, subst, types, cnt):
    if type(v) == tuple:
        return tuple(reify_value(e, subst, types, cnt) for e in v)
    return type(v)._make(reify_value(e, subst, types, cnt) for e in v)


register(tuple, occurs=_tuple_occurs, unify=_tuple, reify=_reify_tuple)
