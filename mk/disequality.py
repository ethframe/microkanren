from .stream import MZero, Unit
from .unify import typeof, unify


def neq(u, v):
    def _goal(state):
        subst, types, cons = state
        a = unify(u, v, subst.copy())
        if a is None:
            return Unit(state)
        if not a:
            return MZero()
        if unify(typeof(u), typeof(v), types.copy()) is None:
            return Unit(state)
        cons[a[0]].append(_goal)
        return Unit(state)
    return _goal


def neqt(v, t):
    def _goal(state):
        subst, types, cons = state
        a = unify(typeof(v), t, types.copy())
        if a is None:
            return Unit(state)
        if not a:
            return MZero()
        cons[a[0]].append(_goal)
        return Unit(state)
    return _goal
