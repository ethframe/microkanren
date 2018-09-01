from .core import Var, assign, walk
from .stream import Cons, Deferred, Empty


def add(a, b, c):
    def _goal(s):
        wa = walk(a, s)
        wb = walk(b, s)
        wc = walk(c, s)
        if isinstance(wa, Var):
            if isinstance(wb, Var):
                return Deferred(Cons(s), _goal)
            if isinstance(wc, Var):
                return Deferred(Cons(s), _goal)
            return Cons(assign(wa, wc - wb, s))
        if isinstance(wb, Var):
            if isinstance(wc, Var):
                return Deferred(Cons(s), _goal)
            return Cons(assign(wb, wc - wa, s))
        if isinstance(wc, Var):
            return Cons(assign(wc, wa + wb, s))
        return Cons(s) if wa + wb == wc else Empty()
    return _goal


def sub(a, b, c):
    return add(b, c, a)


def pred(a, b, p):
    def _goal(s):
        wa = walk(a, s)
        wb = walk(b, s)
        if isinstance(wa, Var) or isinstance(wb, Var):
            return Deferred(Cons(s), _goal)
        return Cons(s) if p(wa, wb) else Empty()
    return _goal


def make_pred(p):
    return lambda a, b: pred(a, b, p)


neq = make_pred(lambda a, b: a != b)
gte = make_pred(lambda a, b: a >= b)
lte = make_pred(lambda a, b: a <= b)
