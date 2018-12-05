from .deferred import make_relation
from .stream import Cons, Cell, Deferred, Empty
from .unify import Var
from .core import do_eq
from .ext import walk_args


@walk_args
def add(goal, state, a, b, c):
    if isinstance(a, Var):
        if isinstance(b, Var) or isinstance(c, Var):
            return Deferred(Cell(state), goal)
        return do_eq(a, c - b, state)
    if isinstance(b, Var):
        if isinstance(c, Var):
            return Deferred(Cell(state), goal)
        return do_eq(b, c - a, state)
    return do_eq(c, a + b, state)


def sub(a, b, c):
    return add(b, c, a)


@walk_args
def mul(goal, state, a, b, c):
    if isinstance(a, Var):
        if isinstance(b, Var) or isinstance(c, Var):
            return Deferred(Cell(state), goal)
        if b == 0:
            return Cell(state) if c == 0 else Empty()
        q, r = divmod(c, b)
        return do_eq(a, q, state) if r == 0 else Empty()
    if isinstance(b, Var):
        if isinstance(c, Var):
            return Deferred(Cell(state), goal)
        if a == 0:
            return Cell(state) if c == 0 else Empty()
        q, r = divmod(c, a)
        return do_eq(b, q, state) if r == 0 else Empty()
    return do_eq(c, a * b, state)


def div(a, b, c):
    return mul(b, c, a)


gte = make_relation(lambda a, b: a >= b)
lte = make_relation(lambda a, b: a <= b)
