from .stream import Cons, Empty
from .unify import Var, unify


def typeof(x):
    if isinstance(x, Var):
        return x
    elif isinstance(x, tuple):
        return (type(x),) + tuple(map(typeof, x))
    return type(x)


def apply_constraints(vs, state):
    cons = state[2]
    stream = Cons(state)
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


def copy(state):
    subst, types, cons = state
    return subst.copy(), types.copy(), {v: cs.copy() for v, cs in cons.items()}


def disj(g1, g2):
    return lambda state: g1(copy(state)).mplus(g2(state))


def conj(g1, g2):
    return lambda state: g1(state).bind(g2)
