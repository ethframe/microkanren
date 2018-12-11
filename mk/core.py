from .stream import Cell, Empty
from .unify import Var, unify, list_as_pairs


def typeof(x):
    if isinstance(x, Var):
        return x
    if isinstance(x, list):
        x = list_as_pairs(x)
    if isinstance(x, tuple):
        return (type(x),) + tuple(map(typeof, x))
    return type(x)


def apply_constraints(vs, state):
    cons = state[2]
    stream = Cell(state)
    for v in vs:
        for g in cons.pop(v, ()):
            stream = stream.bind(g)
    return stream


def do_eq(u, v, state):
    subst, types, cons = state
    a = unify(u, v, subst)
    if a is None:
        return Empty()
    if unify(typeof(u), typeof(v), types) is None:
        return Empty()
    return apply_constraints(a, state)


def eq(u, v):
    return lambda state: do_eq(u, v, state)


def eqt(u, v):
    def _goal(state):
        subst, types, cons = state
        a = unify(typeof(u), v, types)
        if a is None:
            return Empty()
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
