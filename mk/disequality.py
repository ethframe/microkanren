from .stream import Cell, Empty
from .unify import typeof, unify


def neq(u, v):
    def _goal(state):
        subst, types, cons = state
        a = unify(u, v, subst.copy())
        if a is None:
            return Cell(state)
        b = unify(typeof(u), typeof(v), types.copy())
        if b is None:
            return Cell(state)
        if a:
            cons[a[0]].append(_goal)
            return Cell(state)
        return Empty()
    return _goal


def neqt(v, t):
    def _goal(state):
        subst, types, cons = state
        a = unify(typeof(v), t, types.copy())
        if a is None:
            return Cell(state)
        if not a:
            return Empty()
        cons[a[0]].append(_goal)
        return Cell(state)
    return _goal
