from .deferred import make_relation
from .stream import Cons, Deferred, Empty
from .unify import Var, walk
from .core import do_eq


def add(a, b, c):
    def _goal(state):
        subst = state[0]
        wa = walk(a, subst)
        wb = walk(b, subst)
        wc = walk(c, subst)
        if isinstance(wa, Var):
            if isinstance(wb, Var) or isinstance(wc, Var):
                return Deferred(Cons(state), _goal)
            return do_eq(wa, wc - wb, state)
        if isinstance(wb, Var):
            if isinstance(wc, Var):
                return Deferred(Cons(state), _goal)
            return do_eq(wb, wc - wa, state)
        return do_eq(wc, wa + wb, state)
    return _goal


def sub(a, b, c):
    return add(b, c, a)


def mul(a, b, c):
    def _goal(state):
        subst = state[0]
        wa = walk(a, subst)
        wb = walk(b, subst)
        wc = walk(c, subst)
        if isinstance(wa, Var):
            if isinstance(wb, Var) or isinstance(wc, Var):
                return Deferred(Cons(state), _goal)
            if wb == 0:
                return Cons(state) if wc == 0 else Empty()
            q, r = divmod(wc, wb)
            return do_eq(wa, q, state) if r == 0 else Empty()
        if isinstance(wb, Var):
            if isinstance(wc, Var):
                return Deferred(Cons(state), _goal)
            if wa == 0:
                return Cons(state) if wc == 0 else Empty()
            q, r = divmod(wc, wa)
            return do_eq(wb, q, state) if r == 0 else Empty()
        return do_eq(wc, wa * wb, state)
    return _goal


def div(a, b, c):
    return mul(b, c, a)


gte = make_relation(lambda a, b: a >= b)
lte = make_relation(lambda a, b: a <= b)
