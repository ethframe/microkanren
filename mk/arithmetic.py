from .core import do_eq
from .deferred import make_relation
from .dsl import walk_args
from .stream import MZero, Unit
from .unify import Var


@walk_args
def add(goal, state, a, b, c):
    if type(a) is Var:
        if type(b) is Var:
            cons = state[2]
            cons[a].append(goal)
            cons[b].append(goal)
            return Unit(state)
        if type(c) is Var:
            cons = state[2]
            cons[a].append(goal)
            cons[c].append(goal)
            return Unit(state)
        return do_eq(a, c - b, state)
    if type(b) is Var:
        if type(c) is Var:
            cons = state[2]
            cons[b].append(goal)
            cons[c].append(goal)
            return Unit(state)
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
            return Unit(state)
        if type(c) is Var:
            cons = state[2]
            cons[a].append(goal)
            cons[c].append(goal)
            return Unit(state)
        if b == 0:
            if c == 0:
                return Unit(state)
            return MZero()
        q, r = divmod(c, b)
        if r == 0:
            return do_eq(a, q, state)
        return MZero()
    if type(b) is Var:
        if type(c) is Var:
            cons = state[2]
            cons[b].append(goal)
            cons[c].append(goal)
            return Unit(state)
        if a == 0:
            if c == 0:
                return Unit(state)
            return MZero()
        q, r = divmod(c, a)
        if r == 0:
            return do_eq(b, q, state)
        return MZero()
    return do_eq(c, a * b, state)


def div(a, b, c):
    return mul(b, c, a)


gte = make_relation(lambda a, b: a >= b)
lte = make_relation(lambda a, b: a <= b)
