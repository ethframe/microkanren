import pytest
from mk.core import conj, eq
from mk.dsl import conde, conjp, delay, disjp, fresh, zzz
from mk.run import initial, reify
from mk.stream import unfold
from mk.unify import Var

a = Var()
b = Var()
c = Var()


def zzz_goal(a, b):
    return conde(
        eq(b, (1, a)),
        (eq(a, 1), zzz(lambda: zzz_goal(2, b)))
    )


@delay
def delay_goal(a, b):
    return conde(
        eq(b, (1, a)),
        (eq(a, 1), delay_goal(2, b))
    )


GOALS_DATA = [
    (conj(eq(a, 1), fresh(lambda x: conj(eq(a, x), eq(x, c)))), c, [1]),
    (
        conj(
            eq(a, 1),
            fresh(2, lambda x, y: conj(eq((x, y), (a, 2)), eq(c, (x, y))))
        ),
        c,
        [(1, 2)]
    ),
    (conjp(eq(a, 1), eq(b, 2), eq(c, (a, b))), c, [(1, 2)]),
    (conjp(disjp(eq(a, 1), eq(a, 2), eq(a, 3)), eq(c, a)), c, [1, 3, 2]),
    (
        conde(
            (eq(a, 1), eq(b, 2), eq(c, a)),
            (eq(a, 2), eq(b, 3), eq(c, b)),
            eq(c, 5),
        ),
        c,
        [1, 5, 3]
    ),
    (zzz_goal(1, c), c, [(1, 1), (1, 2)]),
    (delay_goal(1, c), c, [(1, 1), (1, 2)]),
]


@pytest.mark.parametrize("goal, query, expected", GOALS_DATA)
def test_dsl(goal, query, expected):
    assert [reify(query, st) for st in unfold(goal(initial()))] == expected
