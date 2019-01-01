import pytest
from mk.stream import Unit, unfold

UNFOLD_DATA = [
    (Unit(1), [1]),
    (Unit(1).mplus(Unit(2)), [1, 2]),
    (Unit(1).mplus(Unit(2).mplus(Unit(3))), [1, 2, 3]),

    (Unit(1).mplus(Unit(2)).mplus(Unit(3)), [1, 3, 2]),

    (Unit(1).bind(lambda a: Unit(a + 1)), [2]),
    (Unit(1).mplus(Unit(2)).bind(lambda a: Unit(a + 1)), [2, 3]),
]


@pytest.mark.parametrize("stream, expected", UNFOLD_DATA)
def test_unfold(stream, expected):
    assert list(unfold(stream)) == expected
