import pytest
from mk.stream import MZero, Thunk, Unit, unfold

UNFOLD_DATA = [
    (MZero(), []),

    (Unit(1), [1]),
    (MZero().mplus(Unit(1)), [1]),

    (Unit(1).mplus(Unit(2)), [1, 2]),
    (Unit(1).mplus(Unit(2).mplus(Unit(3))), [1, 2, 3]),

    (Unit(1).mplus(Unit(2)).mplus(Unit(3)), [1, 3, 2]),

    (Unit(1).bind(lambda a: Unit(a + 1)), [2]),
    (Unit(1).mplus(Unit(2)).bind(lambda a: Unit(a + 1)), [2, 3]),

    (Thunk(lambda: Unit(1)).mplus(Thunk(lambda: Unit(2))), [1, 2]),
]


@pytest.mark.parametrize("stream, expected", UNFOLD_DATA)
def test_unfold(stream, expected):
    assert list(unfold(stream)) == expected
