from .stream import MZero, Unit
from .unify import Var, walk


def predicate(a, p):
    def _goal(state):
        subst, _, cons = state
        wa = walk(a, subst)
        if type(wa) is Var:
            cons[wa].append(_goal)
            return Unit(state)
        if p(wa):
            return Unit(state)
        return MZero()
    return _goal


def make_predicate(p):
    return lambda a: predicate(a, p)


def relation(a, b, p):
    def _goal(state):
        subst, _, cons = state
        wa = walk(a, subst)
        if type(wa) is Var:
            cons[wa].append(_goal)
            return Unit(state)
        wb = walk(b, subst)
        if type(wb) is Var:
            cons[wb].append(_goal)
            return Unit(state)
        if p(wa, wb):
            return Unit(state)
        return MZero()
    return _goal


def make_relation(p):
    return lambda a, b: relation(a, b, p)
