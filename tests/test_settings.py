import pytest

from presidents_quiz.main import NUM_PRESIDENTS, QuizSettings


def test_defaults() -> None:
    s = QuizSettings()
    assert s.repeat_questions is False
    assert s.end_early is False
    # Defaults to full range using the module's NUM_PRESIDENTS (+1 for slicing stop)
    assert s.president_range == (1, NUM_PRESIDENTS + 1)
    assert s.verbose_level == QuizSettings.VERBOSE_NORMAL  # 1


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
    s = QuizSettings(president_range=rng)
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
    s = QuizSettings(president_range=rng)
    assert s.president_range == (1, NUM_PRESIDENTS + 1)


@pytest.mark.parametrize(
    ("level", "expected"),
    [
        (None, QuizSettings.VERBOSE_NORMAL),   # default path -> 1
        (QuizSettings.VERBOSE_QUIET, QuizSettings.VERBOSE_QUIET),       # 0
        (QuizSettings.VERBOSE_NORMAL, QuizSettings.VERBOSE_NORMAL),     # 1
        (QuizSettings.VERBOSE_VERBOSE, QuizSettings.VERBOSE_VERBOSE),   # 2
        (99, QuizSettings.VERBOSE_NORMAL),  # coerced to 1 if not in (0,1,2)
        (-1, QuizSettings.VERBOSE_NORMAL),
    ],
)
def test_verbose_level_handling(level: int | None, expected: int) -> None:
    s = QuizSettings() if level is None else QuizSettings(verbose_level=level)
    assert s.verbose_level == expected


def test_flags_and_pretty_print_format() -> None:
    s = QuizSettings(
        repeat_questions=True,
        end_early=True,
        president_range=(3, 10),
        verbose_level=QuizSettings.VERBOSE_VERBOSE,
        allow_ambiguity=False,
    )
    # ensure values stick (range is valid so no fallback)
    assert s.repeat_questions is True
    assert s.end_early is True
    assert s.president_range == (3, 10)
    assert s.verbose_level == QuizSettings.VERBOSE_VERBOSE
    assert s.allow_ambiguity is False

    # pretty_print should match exact formatting
    expected = "repeat_questions=True, end_early=True, president_range=(3, 10), verbose_level=2, allow_ambiguity=False"
    assert s.pretty_print() == expected
