import pytest
from mk.arithmetic import add, div, gte, lte, mul, sub
from mk.core import conj, eq
from mk.run import initial
from mk.stream import unfold
from mk.unify import Var

a = Var()
b = Var()
c = Var()

GOALS_DATA = [
    (add(1, 2, a), [{a: 3}]),
    (add(1, a, 3), [{a: 2}]),
    (add(a, 2, 3), [{a: 1}]),
    (conj(add(1, a, b), eq(a, 2)), [{a: 2, b: 3}]),
    (conj(add(a, 2, b), eq(a, 1)), [{a: 1, b: 3}]),
    (conj(add(a, b, 3), eq(a, 1)), [{a: 1, b: 2}]),
    (conj(conj(add(a, b, c), eq(a, 1)), eq(b, 2)), [{a: 1, b: 2, c: 3}]),
    (conj(conj(add(a, b, c), eq(a, 1)), eq(c, 3)), [{a: 1, b: 2, c: 3}]),
    (conj(conj(add(a, b, c), eq(b, 2)), eq(c, 3)), [{a: 1, b: 2, c: 3}]),

    (sub(3, 2, a), [{a: 1}]),

    (mul(2, 3, a), [{a: 6}]),
    (mul(2, a, 6), [{a: 3}]),
    (mul(a, 3, 6), [{a: 2}]),
    (conj(mul(2, a, b), eq(a, 3)), [{a: 3, b: 6}]),
    (conj(mul(a, 3, b), eq(a, 2)), [{a: 2, b: 6}]),
    (conj(mul(a, b, 6), eq(a, 2)), [{a: 2, b: 3}]),
    (conj(conj(mul(a, b, c), eq(a, 2)), eq(b, 3)), [{a: 2, b: 3, c: 6}]),
    (conj(conj(mul(a, b, c), eq(a, 2)), eq(c, 6)), [{a: 2, b: 3, c: 6}]),
    (conj(conj(mul(a, b, c), eq(b, 3)), eq(c, 6)), [{a: 2, b: 3, c: 6}]),

    (mul(a, 0, 0), [{}]),
    (mul(a, 0, 1), []),
    (mul(a, 1, 0), [{a: 0}]),
    (mul(a, 2, 4), [{a: 2}]),
    (mul(a, 2, 3), []),

    (mul(0, a, 0), [{}]),
    (mul(0, a, 1), []),
    (mul(1, a, 0), [{a: 0}]),
    (mul(2, a, 4), [{a: 2}]),
    (mul(2, a, 3), []),

    (div(6, 3, a), [{a: 2}]),

    (conj(gte(a, 1), eq(a, 1)), [{a: 1}]),
    (conj(gte(a, 1), eq(a, 2)), [{a: 2}]),
    (conj(gte(a, 1), eq(a, 0)), []),

    (conj(gte(1, a), eq(a, 1)), [{a: 1}]),
    (conj(gte(1, a), eq(a, 0)), [{a: 0}]),
    (conj(gte(1, a), eq(a, 2)), []),

    (conj(lte(a, 1), eq(a, 1)), [{a: 1}]),
    (conj(lte(a, 1), eq(a, 0)), [{a: 0}]),
    (conj(lte(a, 1), eq(a, 2)), []),
]


@pytest.mark.parametrize("goal, expected", GOALS_DATA)
def test_arithmetic(goal, expected):
    assert [s for s, _, _ in unfold(goal(initial()))] == expected
