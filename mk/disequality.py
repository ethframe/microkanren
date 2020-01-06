from .stream import MZero, Unit
from .unify import Var, unify, walk


def neq(u, v):
    def _goal(state):
        subst, types, cons = state
        a = unify(u, v, subst.copy())
        if a is None:
            return Unit(state)
        if not a:
            return MZero()
        cons[a[0]].append(_goal)
        return Unit(state)
    return _goal


def neqt(v, t):
    def _goal(state):
        subst, types, cons = state
        x = walk(v, subst)
        t_x = type(x)
        if t_x is Var:
            t_x = types.get(x)
            if t_x is None:
                cons[x].append(_goal)
                return Unit(state)
            elif t_x is t:
                return MZero()
        elif t_x is t:
            return MZero()
        return Unit(state)
    return _goal
