from .deferred import make_relation
from .stream import Cell, Empty
from .unify import Var
from .core import do_eq
from .ext import walk_args


@walk_args
def add(goal, state, a, b, c):
    if type(a) is Var:
        if type(b) is Var:
            cons = state[2]
            cons[a].append(goal)
            cons[b].append(goal)
            return Cell(state)
        if type(c) is Var:
            cons = state[2]
            cons[a].append(goal)
            cons[c].append(goal)
            return Cell(state)
        return do_eq(a, c - b, state)
    if type(b) is Var:
        if type(c) is Var:
            cons = state[2]
            cons[b].append(goal)
            cons[c].append(goal)
            return Cell(state)
        return do_eq(b, c - a, state)
    return do_eq(c, a + b, state)


def sub(a, b, c):
    return add(b, c, a)


@walk_args
def mul(goal, state, a, b, c):
    if type(a) is Var:
        if type(b) is Var:
            cons = state[2]
            cons[a].append(goal)
            cons[b].append(goal)
            return Cell(state)
        if type(c) is Var:
            cons = state[2]
            cons[a].append(goal)
            cons[c].append(goal)
            return Cell(state)
        if b == 0:
            return Cell(state) if c == 0 else Empty()
        q, r = divmod(c, b)
        return do_eq(a, q, state) if r == 0 else Empty()
    if type(b) is Var:
        if type(c) is Var:
            cons = state[2]
            cons[b].append(goal)
            cons[c].append(goal)
            return Cell(state)
        if a == 0:
            return Cell(state) if c == 0 else Empty()
        q, r = divmod(c, a)
        return do_eq(b, q, state) if r == 0 else Empty()
    return do_eq(c, a * b, state)


def div(a, b, c):
    return mul(b, c, a)


gte = make_relation(lambda a, b: a >= b)
lte = make_relation(lambda a, b: a <= b)
