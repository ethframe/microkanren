from .constraints import make_relation
from .core import Var, assign, walk
from .stream import Cons, Deferred, Empty


def add(a, b, c):
    def _goal(s):
        wa = walk(a, s)
        wb = walk(b, s)
        wc = walk(c, s)
        if isinstance(wa, Var):
            if isinstance(wb, Var) or isinstance(wc, Var):
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


def mul(a, b, c):
    def _goal(s):
        wa = walk(a, s)
        wb = walk(b, s)
        wc = walk(c, s)
        if isinstance(wa, Var):
            if isinstance(wb, Var) or isinstance(wc, Var):
                return Deferred(Cons(s), _goal)
            if wb == 0:
                return Cons(s) if wc == 0 else Empty()
            q, r = divmod(wc, wb)
            return Cons(assign(wa, q, s)) if r == 0 else Empty()
        if isinstance(wb, Var):
            if isinstance(wc, Var):
                return Deferred(Cons(s), _goal)
            if wa == 0:
                return Cons(s) if wc == 0 else Empty()
            q, r = divmod(wc, wa)
            return Cons(assign(wb, q, s)) if r == 0 else Empty()
        if isinstance(wc, Var):
            return Cons(assign(wc, wa * wb, s))
        return Cons(s) if wa * wb == wc else Empty()
    return _goal


def div(a, b, c):
    return mul(b, c, a)


gte = make_relation(lambda a, b: a >= b)
lte = make_relation(lambda a, b: a <= b)
