import logging

import pytest  # noqa: TC002 3.10 - 3.13 fail with type checking block because they don't have lazy annotation evaluation

from presidents_quiz.presidents import (
    GEORGE_H_W_BUSH,
    GEORGE_W_BUSH,
    GEORGE_WASHINGTON,
    GROVER_CLEVELAND,
    JAMES_K_POLK,
    JOHN_ADAMS,
    JOHN_QUINCY_ADAMS,
    LYNDON_B_JOHNSON,
    MARTIN_VANBUREN,
    RICHARD_NIXON,
    THEODORE_ROOSEVELT,
    WILLIAM_MCKINLEY,
    President,
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

def test_check_name_allows_buren_for_van_buren_when_ambiguous_flag_true() -> None:
    p = MARTIN_VANBUREN
    assert p.check_name("Buren", allow_ambiguity=True) is True


def test_check_name_rejects_buren_for_van_buren_when_ambiguous_flag_false() -> None:
    p = MARTIN_VANBUREN
    assert p.check_name("Buren", allow_ambiguity=False) is False


# check_name

def test_check_name_accepts_first_last_simple() -> None:
    assert GEORGE_WASHINGTON.check_name("George Washington", allow_ambiguity=False) is True


def test_check_name_accepts_first_middle_last_ignoring_periods_and_spaces() -> None:
    assert JAMES_K_POLK.check_name("James K. Polk", allow_ambiguity=False) is True
    assert JAMES_K_POLK.check_name("James K Polk", allow_ambiguity=False) is True  # dots removed
    assert JAMES_K_POLK.check_name("  James K. Polk  ", allow_ambiguity=False) is True  # edges stripped
    assert JAMES_K_POLK.check_name(" James K Polk  ", allow_ambiguity=False) is True  # dots removed and edges stripped


def test_check_name_accepts_middle_last() -> None:
    assert JOHN_QUINCY_ADAMS.check_name("Quincy Adams", allow_ambiguity=False) is True


def test_check_name_accepts_nickname() -> None:
    assert THEODORE_ROOSEVELT.check_name("Teddy", allow_ambiguity=False) is True


def test_check_name_accepts_last_only_when_unambiguous() -> None:
    assert RICHARD_NIXON.check_name("Nixon", allow_ambiguity=False) is True


def test_check_name_rejects_ambiguous_last_name_and_warns(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level("WARNING"):
        ok = LYNDON_B_JOHNSON.check_name("Johnson", allow_ambiguity=False)
    assert ok is False
    # verify warning about ambiguity is emitted
    assert any("Ambiguous name provided" in rec.getMessage() for rec in caplog.records)


def test_check_name_rejects_ambiguous_full_name_for_both_bushes_and_warns(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level("WARNING"):
        ok41 = GEORGE_H_W_BUSH.check_name("George Bush", allow_ambiguity=False)
        ok43 = GEORGE_W_BUSH.check_name("George Bush", allow_ambiguity=False)
    assert ok41 is False
    assert ok43 is False
    assert any("Ambiguous name provided" in rec.getMessage() for rec in caplog.records)


def test_check_name_half_ambiguous_john_adams_rules() -> None:
    # Intended behavior: plain "John Adams" should match ONLY the elder John Adams
    assert JOHN_ADAMS.check_name("John Adams", allow_ambiguity=False) is True
    assert JOHN_QUINCY_ADAMS.check_name("John Adams", allow_ambiguity=False) is False

# check_name with -a flag

def test_ambiguous_fullname_bush_rejected_by_default_and_warns(caplog: pytest.LogCaptureFixture) -> None:
    # default is allow_ambiguity=False
    caplog.set_level(logging.WARNING)
    ok41 = GEORGE_H_W_BUSH.check_name("George Bush", allow_ambiguity=False)
    ok43 = GEORGE_W_BUSH.check_name("George Bush", allow_ambiguity=False)

    assert not ok41
    assert not ok43
    assert any("Ambiguous name provided" in r.getMessage() for r in caplog.records)


def test_ambiguous_fullname_bush_allowed_with_flag_and_debug_logged(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.DEBUG)

    ok41 = GEORGE_H_W_BUSH.check_name("George Bush", allow_ambiguity=True)
    ok43 = GEORGE_W_BUSH.check_name("George Bush", allow_ambiguity=True)

    assert ok41
    assert ok43
    # message flips to DEBUG and includes the "allowed" suffix
    assert any("Allowed because of -a flag" in r.getMessage() for r in caplog.records)


def test_half_ambiguous_john_adams_for_jqa_depends_on_flag() -> None:
    # Without -a: "John Adams" should NOT match John Quincy Adams
    assert JOHN_QUINCY_ADAMS.check_name("John Adams", allow_ambiguity=False) is False
    # With -a: it SHOULD match John Quincy Adams
    assert JOHN_QUINCY_ADAMS.check_name("John Adams", allow_ambiguity=True) is True
    # And the elder John Adams continues to match either way
    assert JOHN_ADAMS.check_name("John Adams", allow_ambiguity=True) is True


def test_ambiguous_lastname_johnson_depends_on_flag(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.WARNING)
    assert LYNDON_B_JOHNSON.check_name("Johnson", allow_ambiguity=False) is False
    assert any("Ambiguous name provided" in r.getMessage() for r in caplog.records)

    caplog.clear()
    caplog.set_level(logging.DEBUG)
    assert LYNDON_B_JOHNSON.check_name("Johnson", allow_ambiguity=True) is True
    assert any("Allowed because of -a flag" in r.getMessage() for r in caplog.records)


# check_order

def test_check_order_single_term_exact_match_and_trim() -> None:
    assert WILLIAM_MCKINLEY.check_order("25") is True
    assert WILLIAM_MCKINLEY.check_order(" 25 ") is True
    assert WILLIAM_MCKINLEY.check_order("24") is False


def test_check_order_multi_term_needs_space_separated_exact_sequence() -> None:
    # Grover Cleveland served non-consecutive terms: "22 24"
    assert GROVER_CLEVELAND.check_order("22 24") is True
    assert GROVER_CLEVELAND.check_order("22") is False
    assert GROVER_CLEVELAND.check_order("22,24") is False  # commas not allowed by implementation
    assert GROVER_CLEVELAND.check_order("24 22") is False  # wrong order


# check_year

def test_check_year_single_term_exact_match_and_trim() -> None:
    assert WILLIAM_MCKINLEY.check_year("1897") is True
    assert WILLIAM_MCKINLEY.check_year(" 1897 ") is True
    assert WILLIAM_MCKINLEY.check_year("1898") is False


def test_check_year_multi_term_needs_space_separated_exact_sequence() -> None:
    # Grover Cleveland: "1885 1893"
    assert GROVER_CLEVELAND.check_year("1885 1893") is True
    assert GROVER_CLEVELAND.check_year("1885") is False
    assert GROVER_CLEVELAND.check_year("1885,1893") is False
    assert GROVER_CLEVELAND.check_year("1893 1885") is False
