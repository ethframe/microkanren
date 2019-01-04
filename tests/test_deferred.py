import pytest
from mk.core import conj, eq
from mk.deferred import predicate, relation
from mk.dsl import conjp
from mk.run import initial
from mk.stream import unfold
from mk.unify import Var

a = Var()
b = Var()

GOALS_DATA = [
    (conj(eq(a, 1), predicate(a, lambda a: a > 0)), [{a: 1}]),
    (conj(predicate(a, lambda a: a > 0), eq(a, 1)), [{a: 1}]),
    (conj(eq(a, 0), predicate(a, lambda a: a > 0)), []),
    (conj(predicate(a, lambda a: a > 0), eq(a, 0)), []),

    (predicate(a, lambda a: a > 0), [{}]),

    (
        conjp(eq(a, 1), eq(b, 0), relation(a, b, lambda a, b: a > b)),
        [{a: 1, b: 0}]
    ),
    (
        conjp(relation(a, b, lambda a, b: a > b), eq(a, 1), eq(b, 0)),
        [{a: 1, b: 0}]
    ),
    (
        conjp(eq(a, 1),  relation(a, b, lambda a, b: a > b), eq(b, 0)),
        [{a: 1, b: 0}]
    ),

    (conjp(eq(a, 1), eq(b, 1), relation(a, b, lambda a, b: a > b)), []),
    (conjp(relation(a, b, lambda a, b: a > b), eq(a, 1), eq(b, 1)), []),
    (conjp(eq(a, 1),  relation(a, b, lambda a, b: a > b), eq(b, 1)), []),

    (conj(eq(a, 1), relation(a, b, lambda a, b: a > b)), [{a: 1}]),
    (conj(relation(a, b, lambda a, b: a > b), eq(a, 1)), [{a: 1}]),
    (conj(relation(a, b, lambda a, b: a > b), eq(a, 1)), [{a: 1}]),

    (relation(a, b, lambda a, b: a > b), [{}]),
]


@pytest.mark.parametrize("goal, expected", GOALS_DATA)
def test_deferred(goal, expected):
    assert [s for s, _, _ in unfold(goal(initial()))] == expected
