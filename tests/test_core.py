import pytest
from mk.core import conj, disj, eq, eqt
from mk.run import initial
from mk.stream import unfold
from mk.unify import Var, convert

a = Var()
b = Var()

GOALS_DATA = [
    (eq(a, 1), [{a: 1}]),
    (disj(eq(a, 1), eq(a, 2)), [{a: 1}, {a: 2}]),
    (conj(eq(a, 1), eq(a, 1)), [{a: 1}]),

    (conj(eq(a, 1), eq(a, 2)), []),

    (eqt(a, int), [{}]),
    (conj(eq(a, 1), eqt(a, int)), [{a: 1}]),
    (conj(eqt(a, int), eq(a, 1)), [{a: 1}]),
    (conj(eq(a, 1), eqt(a, str)), []),
    (conj(eqt(a, str), eq(a, 1)), []),

    (conj(eqt(a, int), eqt(a, int)), [{}]),
    (conj(eqt(a, int), eqt(a, str)), []),

    (conj(conj(eqt(a, int), eqt(b, int)), eq(a, b)), [{a: b}]),
    (conj(conj(eqt(a, int), eqt(b, str)), eq(a, b)), []),

    (conj(conj(eq(a, [1]), eq(b, 1)), eq(a, [b])), [{a: convert([1]), b: 1}]),
    (conj(conj(eq(a, [b]), eq(b, 1)), eq(a, [1])), [{a: convert([b]), b: 1}]),
    (conj(conj(eq(a, [b]), eq(b, 1)), eq(a, [2])), [])
]


@pytest.mark.parametrize("goal, expected", GOALS_DATA)
def test_goals(goal, expected):
    assert [s for s, _, _ in unfold(goal(initial()))] == expected
