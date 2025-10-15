import pytest  # noqa: TC002 3.10 - 3.13 fail with type checking block because they don't have lazy annotation evaluation

from main import President, check_name, check_order, check_year
from presidents import (
    GEORGE_H_W_BUSH,
    GEORGE_W_BUSH,
    GEORGE_WASHINGTON,
    GROVER_CLEVELAND,
    JAMES_K_POLK,
    JOHN_ADAMS,
    JOHN_QUINCY_ADAMS,
    LYNDON_B_JOHNSON,
    RICHARD_NIXON,
    THEODORE_ROOSEVELT,
    WILLIAM_MCKINLEY,
)


def test_president_init_basic() -> None:
    p = President("George", "Washington", ["1"], ["1789"])
    assert p.first_name == "George"
    assert p.last_name == "Washington"
    assert p.order_numbers == ["1"]
    assert p.start_year == ["1789"]
    assert p.middle_name is None
    assert p.nickname is None

def test_president_init_with_middle_and_nickname() -> None:
    p = President("Theodore", "Roosevelt", ["26"], ["1901"], nickname="Teddy")
    assert p.nickname == "Teddy"
    assert p.middle_name is None

    p2 = President("John", "Adams", ["6"], ["1825"], middle_name="Quincy")
    assert p2.middle_name == "Quincy"

def test_president_str_and_get_president_name() -> None:
    p = President("John", "Adams", ["2"], ["1797"])
    assert str(p) == p.get_president_name()
    assert p.get_president_name() == "John Adams"

def test_is_full_name_ambiguous() -> None:
    p = President("George", "Bush", ["41"], ["1989"])
    assert p.is_full_name_ambiguous() is True

    p2 = President("John", "Adams", ["2"], ["1797"])
    assert p2.is_full_name_ambiguous() is False

def test_is_last_name_ambiguous() -> None:
    p = President("George", "Bush", ["41"], ["1989"])
    assert p.is_last_name_ambiguous() is True

    p2 = President("Barack", "Obama", ["44"], ["2009"])
    assert p2.is_last_name_ambiguous() is False

def test_is_year_ambiguous() -> None:
    p = President("William", "Harrison", ["9"], ["1841"])
    assert p.is_year_ambiguous() is True

    p2 = President("Barack", "Obama", ["44"], ["2009"])
    assert p2.is_year_ambiguous() is False

def test_president_with_multiple_order_numbers_and_years() -> None:
    p = President("Grover", "Cleveland", ["22", "24"], ["1885", "1893"])
    assert p.order_numbers == ["22", "24"]
    assert p.start_year == ["1885", "1893"]

# ---------- check_name --------------------------------------------------------

def test_check_name_accepts_first_last_simple() -> None:
    assert check_name("George Washington", GEORGE_WASHINGTON) is True


def test_check_name_accepts_first_middle_last_ignoring_periods_and_spaces() -> None:
    assert check_name("James K. Polk", JAMES_K_POLK) is True
    assert check_name("James K Polk", JAMES_K_POLK) is True  # dots removed
    assert check_name("  James K. Polk  ", JAMES_K_POLK) is True  # edges stripped
    assert check_name(" James K Polk  ", JAMES_K_POLK) is True  # dots removed and edges stripped


def test_check_name_accepts_middle_last() -> None:
    assert check_name("Quincy Adams", JOHN_QUINCY_ADAMS) is True


def test_check_name_accepts_nickname() -> None:
    assert check_name("Teddy", THEODORE_ROOSEVELT) is True


def test_check_name_accepts_last_only_when_unambiguous() -> None:
    assert check_name("Nixon", RICHARD_NIXON) is True


def test_check_name_rejects_ambiguous_last_name_and_warns(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level("WARNING"):
        ok = check_name("Johnson", LYNDON_B_JOHNSON)
    assert ok is False
    # verify warning about ambiguity is emitted
    assert any("Ambiguous name provided" in rec.getMessage() for rec in caplog.records)


def test_check_name_rejects_ambiguous_full_name_for_both_bushes_and_warns(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level("WARNING"):
        ok41 = check_name("George Bush", GEORGE_H_W_BUSH)
        ok43 = check_name("George Bush", GEORGE_W_BUSH)
    assert ok41 is False
    assert ok43 is False
    assert any("Ambiguous name provided" in rec.getMessage() for rec in caplog.records)


def test_check_name_half_ambiguous_john_adams_rules() -> None:
    # Intended behavior: plain "John Adams" should match ONLY the elder John Adams
    assert check_name("John Adams", JOHN_ADAMS) is True
    assert check_name("John Adams", JOHN_QUINCY_ADAMS) is False


# ---------- check_order -------------------------------------------------------

def test_check_order_single_term_exact_match_and_trim() -> None:
    assert check_order("25", WILLIAM_MCKINLEY) is True
    assert check_order(" 25 ", WILLIAM_MCKINLEY) is True
    assert check_order("24", WILLIAM_MCKINLEY) is False


def test_check_order_multi_term_needs_space_separated_exact_sequence() -> None:
    # Grover Cleveland served non-consecutive terms: "22 24"
    assert check_order("22 24", GROVER_CLEVELAND) is True
    assert check_order("22", GROVER_CLEVELAND) is False
    assert check_order("22,24", GROVER_CLEVELAND) is False  # commas not allowed by implementation
    assert check_order("24 22", GROVER_CLEVELAND) is False  # wrong order


# ---------- check_year --------------------------------------------------------

def test_check_year_single_term_exact_match_and_trim() -> None:
    assert check_year("1897", WILLIAM_MCKINLEY) is True
    assert check_year(" 1897 ", WILLIAM_MCKINLEY) is True
    assert check_year("1898", WILLIAM_MCKINLEY) is False


def test_check_year_multi_term_needs_space_separated_exact_sequence() -> None:
    # Grover Cleveland: "1885 1893"
    assert check_year("1885 1893", GROVER_CLEVELAND) is True
    assert check_year("1885", GROVER_CLEVELAND) is False
    assert check_year("1885,1893", GROVER_CLEVELAND) is False
    assert check_year("1893 1885", GROVER_CLEVELAND) is False
