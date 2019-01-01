import pytest
from mk.core import conj, eq, eqt
from mk.disequality import neq, neqt
from mk.run import initial
from mk.stream import unfold
from mk.unify import Var

a = Var()
b = Var()

GOALS_DATA = [
    (neq(a, 1), [{}]),
    (conj(eq(a, 1), neq(a, 2)), [{a: 1}]),
    (conj(eq(a, 1), neq(a, 1)), []),
    (conj(neq(a, 1), eq(a, 1)), []),

    (conj(conj(eq(a, 1), neq(a, b)), eqt(b, str)), [{a: 1}]),

    (neqt(a, int), [{}]),
    (conj(eq(a, 1), neqt(a, str)), [{a: 1}]),
    (conj(eqt(a, int), neqt(a, str)), [{}]),
    (conj(eq(a, 1), neqt(a, int)), []),
    (conj(eqt(a, int), neqt(a, int)), []),
    (conj(neqt(a, int), eq(a, 1)), []),
    (conj(neqt(a, int), eqt(a, int)), []),
]


@pytest.mark.parametrize("goal, expected", GOALS_DATA)
def test_disequality(goal, expected):
    assert [s for s, _, _ in unfold(goal(initial()))] == expected
