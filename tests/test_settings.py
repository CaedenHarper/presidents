import pytest

from main import NUM_PRESIDENTS, Settings


def test_defaults() -> None:
    s = Settings()
    assert s.repeat_questions is False
    assert s.end_early is False
    # Defaults to full range using the module's NUM_PRESIDENTS (+1 for slicing stop)
    assert s.president_range == (1, NUM_PRESIDENTS + 1)
    assert s.verbose_level == Settings.VERBOSE_NORMAL  # 1


@pytest.mark.parametrize(
    "rng",
    [
        (1, 2),
        (1, 1),  # degenerate but allowed by constructor guard (start <= end)
        (2, 5),
        (1, NUM_PRESIDENTS + 1),  # upper bound allowed by guard
    ],
)
def test_valid_range_is_kept(rng: tuple[int, int]) -> None:
    s = Settings(president_range=rng)
    assert s.president_range == rng


@pytest.mark.parametrize(
    "rng",
    [
        (0, 2),  # start < 1
        (2, 1),  # start > end
        (1, NUM_PRESIDENTS + 2),  # end > NUM_PRESIDENTS + 1
    ],
)
def test_invalid_range_falls_back_to_default(rng: tuple[int, int]) -> None:
    s = Settings(president_range=rng)
    assert s.president_range == (1, NUM_PRESIDENTS + 1)


@pytest.mark.parametrize(
    ("level", "expected"),
    [
        (None, Settings.VERBOSE_NORMAL),   # default path -> 1
        (Settings.VERBOSE_QUIET, Settings.VERBOSE_QUIET),       # 0
        (Settings.VERBOSE_NORMAL, Settings.VERBOSE_NORMAL),     # 1
        (Settings.VERBOSE_VERBOSE, Settings.VERBOSE_VERBOSE),   # 2
        (99, Settings.VERBOSE_NORMAL),  # coerced to 1 if not in (0,1,2)
        (-1, Settings.VERBOSE_NORMAL),
    ],
)
def test_verbose_level_handling(level: int | None, expected: int) -> None:
    s = Settings() if level is None else Settings(verbose_level=level)
    assert s.verbose_level == expected


def test_flags_and_pretty_print_format() -> None:
    s = Settings(
        repeat_questions=True,
        end_early=True,
        president_range=(3, 10),
        verbose_level=Settings.VERBOSE_VERBOSE,
    )
    # ensure values stick (range is valid so no fallback)
    assert s.repeat_questions is True
    assert s.end_early is True
    assert s.president_range == (3, 10)
    assert s.verbose_level == Settings.VERBOSE_VERBOSE

    # pretty_print should match exact formatting
    expected = (
        f"repeat_questions={s.repeat_questions}, "
        f"end_early={s.end_early}, "
        f"president_range={s.president_range}, "
        f"verbose_level={s.verbose_level}"
    )
    assert s.pretty_print() == expected
