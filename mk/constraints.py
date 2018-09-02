from .core import Var, walk
from .stream import Cons, Deferred, Empty


def predicate(a, p):
    def _goal(s):
        wa = walk(a, s)
        if isinstance(wa, Var):
            return Deferred(Cons(s), _goal)
        return Cons(s) if p(wa) else Empty()
    return _goal


def make_predicate(p):
    return lambda a: predicate(a, p)


def relation(a, b, p):
    def _goal(s):
        wa = walk(a, s)
        wb = walk(b, s)
        if isinstance(wa, Var) or isinstance(wb, Var):
            return Deferred(Cons(s), _goal)
        return Cons(s) if p(wa, wb) else Empty()
    return _goal


def make_relation(p):
    return lambda a, b: relation(a, b, p)


neq = make_relation(lambda a, b: a != b)
