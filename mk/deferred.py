from .stream import Cons, Cell, Deferred, Empty
from .unify import Var, walk


def predicate(a, p):
    def _goal(state):
        subst = state[0]
        wa = walk(a, subst)
        if isinstance(wa, Var):
            return Deferred(Cell(state), _goal)
        return Cell(state) if p(wa) else Empty()
    return _goal


def make_predicate(p):
    return lambda a: predicate(a, p)


def relation(a, b, p):
    def _goal(state):
        subst = state[0]
        wa = walk(a, subst)
        wb = walk(b, subst)
        if isinstance(wa, Var) or isinstance(wb, Var):
            return Deferred(Cell(state), _goal)
        return Cell(state) if p(wa, wb) else Empty()
    return _goal


def make_relation(p):
    return lambda a, b: relation(a, b, p)
