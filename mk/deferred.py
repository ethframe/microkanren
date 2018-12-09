from .stream import Cell, Empty
from .unify import Var, walk


def predicate(a, p):
    def _goal(state):
        subst, _, cons = state
        wa = walk(a, subst)
        if type(wa) is Var:
            cons.setdefault(wa, []).append(_goal)
            return Cell(state)
        return Cell(state) if p(wa) else Empty()
    return _goal


def make_predicate(p):
    return lambda a: predicate(a, p)


def relation(a, b, p):
    def _goal(state):
        subst, _, cons = state
        wa = walk(a, subst)
        if type(wa) is Var:
            cons.setdefault(wa, []).append(_goal)
            return Cell(state)
        wb = walk(b, subst)
        if type(wb) is Var:
            cons.setdefault(wb, []).append(_goal)
            return Cell(state)
        return Cell(state) if p(wa, wb) else Empty()
    return _goal


def make_relation(p):
    return lambda a, b: relation(a, b, p)
