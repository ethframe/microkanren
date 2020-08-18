from functools import reduce, wraps

from .core import copy
from .run import run
from .stream import Stream
from .unify import Var, walk


def fresh(fst, *args):
    if not args:
        return fst(Var())
    (fn,) = args
    return fn(*(Var() for _ in range(fst)))


def conjp(g, *gs):
    return lambda state: reduce(
        lambda s, g: s.bind(g), gs, g(state)
    )


def disjp(g, *gs):
    return lambda state: reduce(
        lambda s, o: s.mplus(o), [g(copy(state)) for g in gs], g(state)
    )


def conde(*ggs):
    return disjp(*(gs if callable(gs) else conjp(*gs) for gs in ggs))


class Apply(Stream):
    __slots__ = ('state', 'goal')

    def __init__(self, state, goal):
        self.state = state
        self.goal = goal

    def mplus(self, stream):
        return Apply(self.state, MPlusGoal(stream, self.goal))

    def bind(self, goal):
        return Apply(self.state, BindGoal(self.goal, goal))

    def next(self):
        return None, self.goal(self.state)


class MPlusGoal:
    __slots__ = ('stream', 'goal')

    def __init__(self, stream, goal):
        self.stream = stream
        self.goal = goal

    def __call__(self, state):
        return self.stream.mplus(self.goal(state))


class BindGoal:
    __slots__ = ('left', 'right')

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, state):
        return self.left(state).bind(self.right)


class Zzz:
    __slots__ = ('fn',)

    def __init__(self, fn):
        self.fn = fn

    def __call__(self, state):
        return self.fn()(state)


def zzz(thunk):
    return lambda state: Apply(state, Zzz(thunk))


class Delay:
    __slots__ = ('fn', 'args')

    def __init__(self, fn, args):
        self.fn = fn
        self.args = args

    def __call__(self, state):
        return self.fn(*self.args)(state)


def delay(fn):
    @wraps(fn)
    def _constructor(*args):
        return lambda state: Apply(state, Delay(fn, args))
    return _constructor


def runp(c, v, *gs):
    return run(c, v, conjp(*gs))


def walk_args(fn):
    @wraps(fn)
    def _constructor(*args):
        def _goal(state):
            subst = state[0]
            return fn(_goal, state, *(walk(a, subst) for a in args))
        return _goal
    return _constructor
