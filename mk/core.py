from .stream import MZero, Unit
from .unify import Var, unify, walk


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
        t_e = types.pop(e, None)
        if t_e is None:
            continue
        x = walk(e, subst)
        t_x = type(x)
        if t_x is Var:
            t_x = types.get(x)
            if t_x is None:
                types[x] = t_e
            elif t_x is not t_e:
                return MZero()
        elif t_x is not t_e:
            return MZero()
    return apply_constraints(a, state)


def eq(u, v):
    return lambda state: do_eq(u, v, state)


def eqt(v, t):
    def _goal(state):
        subst, types, cons = state
        x = walk(v, subst)
        t_x = type(x)
        if t_x is Var:
            t_x = types.get(x)
            if t_x is None:
                types[x] = t
                return apply_constraints([x], state)
            elif t_x is not t:
                return MZero()
        elif t_x is not t:
            return MZero()
        return Unit(state)
    return _goal


class WatchList(dict):
    def __missing__(self, item):
        ls = self[item] = []
        return ls

    def copy(self):
        return WatchList((k, v.copy()) for k, v in self.items())


def initial():
    return {}, {}, WatchList()


def copy(state):
    subst, types, cons = state
    return subst.copy(), types.copy(), cons.copy()


def disj(g1, g2):
    return lambda state: g1(copy(state)).mplus(g2(state))


def conj(g1, g2):
    return lambda state: g1(state).bind(g2)
