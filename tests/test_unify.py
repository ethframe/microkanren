import pytest
from mk.unify import Var, convert, unify

u = Var()
v = Var()


UNIFY_DATA = [
    (u, 1, {}, [u], {u: 1}),
    (u, 1, {u: 1}, [], {u: 1}),
    (u, 1, {u: 2}, None, None),

    (1, v, {}, [v], {v: 1}),
    (1, v, {v: 1}, [], {v: 1}),
    (1, v, {v: 2}, None, None),

    (u, v, {}, [u], {u: v}),
    (u, u, {}, [], {}),

    (u, (1, 2), {}, [u], {u: (1, 2)}),

    ((u, v), (1, 2), {}, [u, v], {u: 1, v: 2}),
    ((u, v), (1, 2), {u: 1}, [v], {u: 1, v: 2}),
    ((u, v), (1, 2), {u: 2}, None, None),

    (u, (1, u), {}, None, None),

    ([u, v], [1, 2], {}, [u, v], {u: 1, v: 2}),
    ([u, v, ...], [1, 2], {}, [u, v], {u: 1, v: convert([2])}),
    ([u, v], (1, 2), {}, None, None),
]


@pytest.mark.parametrize("u, v, subst, expected, extended", UNIFY_DATA)
def test_unify(u, v, subst, expected, extended):
    assert unify(u, v, subst) == expected
    if expected is not None:
        assert subst == extended
