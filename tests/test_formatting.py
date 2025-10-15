import pytest

from formatting import format_as_percent

# format_as_percent

@pytest.mark.parametrize(
    ("n","d","expected"),
    [
        (0, 1, "0.00%"),
        (1, 4, "25.00%"),
        (1, 3, "33.33%"),  # rounding
        (2, 3, "66.67%"),
        (5, 0, "0.00%"),   # d == 0 -> 0
        (5, -2, "0.00%"),  # d < 0 -> 0 (per current implementation)
    ],
)
def test_format_as_percent(n: int, d: int, expected: str) -> None:
    assert format_as_percent(n, d) == expected
