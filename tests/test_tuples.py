from collections import namedtuple

import pytest
from mk.core import conj, eq
from mk.dsl import conjp
from mk.ext.tuples import no_item
from mk.run import initial, reify
from mk.stream import unfold
from mk.unify import Var

a = Var()
b = Var()


Tuple = namedtuple("Tuple", "x, y")


GOALS_DATA = [
    (eq(a, ()), a, [()]),
    (eq(a, (1,)), a, [(1,)]),
    (conj(eq(a, (b,)), eq(b, 1)), a, [(1,)]),
    (eq(a, (a,)), a, []),

    (conjp(eq(a, (1,)), eq(b, (1,)), eq(a, b)), a, [(1,)]),
    (conjp(eq(a, (1,)), eq(b, (2,)), eq(a, b)), a, []),
    (conjp(eq(a, (1,)), eq(b, (1, 2)), eq(a, b)), a, []),
    (conjp(eq(a, (1,)), eq(b, ()), eq(a, b)), a, []),

    (conj(eq(a, Tuple(1, 2)), eq(a, Tuple(1, 2))), a, [Tuple(1, 2)]),
    (conj(eq(a, Tuple(1, 1)), eq(a, Tuple(1, 2))), a, []),
    (conj(eq(a, Tuple(1, 2)), eq(a, (1, 2))), a, []),

    (no_item((1, 2, 3), lambda v: v == 0), None, [None]),
    (no_item((1, 2, 3), lambda v: v == 1), None, []),
    (conj(no_item(a, lambda v: v == 0), eq(a, (1, 2, 3))), None, [None]),
    (conj(no_item(a, lambda v: v == 1), eq(a, (1, 2, 3))), None, []),

    (no_item((1, (1, 2), (1, 2, (1, 2, 3))), lambda v: v == 0), None, [None]),
    (no_item((1, (1, 2), (1, 2, (1, 2, 3))), lambda v: v == 3), None, []),
]


@pytest.mark.parametrize("goal, query, expected", GOALS_DATA)
def test_lists(goal, query, expected):
    assert [reify(query, st) for st in unfold(goal(initial()))] == expected
