from collections import namedtuple

import pytest
from mk.core import eq, eqt
from mk.dsl import conjp
from mk.run import run
from mk.unify import Var

a = Var()
b = Var()

RUN_DATA = [
    (eq(a, 1), a, 1),
    (conjp(eq(a, (1, b)), eq(b, 2)), a, (1, 2)),
    (conjp(eq(a, (1, b)), eq(b, 2)), (a, b), ((1, 2), 2)),
]


@pytest.mark.parametrize("goal, query, expected", RUN_DATA)
def test_run(goal, query, expected):
    assert next(run(0, query, goal)) == expected


Tuple = namedtuple("Tuple", "a, b")


REIFY_DATA = [
    (eq(a, a), a, '_0:_0'),
    (eq(a, (1, b)), a, '(1, _0:_0)'),
    (eq(a, Tuple(1, b)), a, 'Tuple(a=1, b=_0:_0)'),
    (eq(a, [1, b]), a, '[1, _0:_0]'),
    (eq(a, [1, b, ...]), a, '[1, _0:_0, Ellipsis]'),
    (eqt(a, int), a, '_0:int'),
    (conjp(eqt(a, int), eq(a, b)), (a, b), '(_0:int, _0:int)'),
]


@pytest.mark.parametrize("goal, query, expected", REIFY_DATA)
def test_reify(goal, query, expected):
    assert repr(next(run(0, query, goal))) == expected
