from .stream import MZero, Unit
from .unify import typeof, unify, walk


def apply_constraints(vs, state):
    cons = state[2]
    stream = Unit(state)
    for v in vs:
        for g in cons.pop(v, ()):
            stream = stream.bind(g)
    return stream


def do_eq(u, v, state):
    subst, types, cons = state
    a = unify(u, v, subst)
    if a is None:
        return MZero()
    for e in a:
        if unify(e, typeof(walk(e, subst)), types) is None:
            return MZero()
    return apply_constraints(a, state)


def eq(u, v):
    return lambda state: do_eq(u, v, state)


def eqt(u, v):
    def _goal(state):
        subst, types, cons = state
        a = unify(typeof(u), v, types)
        if a is None:
            return MZero()
        return apply_constraints(a, state)
    return _goal


class WatchList(dict):
    def __missing__(self, item):
        ls = self[item] = []
        return ls

    def copy(self):
        return WatchList((k, v.copy()) for k, v in self.items())


def copy(state):
    subst, types, cons = state
    return subst.copy(), types.copy(), cons.copy()


def disj(g1, g2):
    return lambda state: g1(copy(state)).mplus(g2(state))


def conj(g1, g2):
    return lambda state: g1(state).bind(g2)
