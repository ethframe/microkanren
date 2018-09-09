from .core import typeof
from .stream import Cons, Empty
from .unify import unify


def neq(u, v):
    def _goal(state):
        subst, types, cons = state
        a = unify(u, v, subst.copy())
        if a is None:
            return Cons(state)
        b = unify(typeof(u), typeof(v), types.copy())
        if b is None:
            return Cons(state)
        if not (a or b):
            return Empty()
        cons.setdefault(a[0], []).append(_goal)
        return Cons(state)
    return _goal


def neqt(v, t):
    def _goal(state):
        subst, types, cons = state
        a = unify(typeof(v), t, types.copy())
        if a is None:
            return Cons(state)
        if not a:
            return Empty()
        cons.setdefault(a[0], []).append(_goal)
        return Cons(state)
    return _goal
