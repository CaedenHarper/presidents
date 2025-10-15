import pytest

from main import format_as_percent, get_name_response, get_order_response, get_response, get_year_response
from presidents import GEORGE_WASHINGTON, GROVER_CLEVELAND

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


# get_year_response

def test_get_year_response_correct() -> None:
    assert get_year_response(GEORGE_WASHINGTON, check_name_result=True, check_order_result=True) == "Correct!"


def test_get_year_response_both_wrong_message_singleton() -> None:
    msg = get_year_response(GEORGE_WASHINGTON, check_name_result=False, check_order_result=False)
    assert msg == "Wrong! The correct answer is president George Washington, order number 1."


def test_get_year_response_only_order_wrong() -> None:
    msg = get_year_response(GEORGE_WASHINGTON, check_name_result=True, check_order_result=False)
    assert msg == "Wrong order number! The correct order number is 1."


def test_get_year_response_only_name_wrong() -> None:
    msg = get_year_response(GEORGE_WASHINGTON, check_name_result=False, check_order_result=True)
    assert msg == "Wrong president! The correct president is George Washington."


def test_get_year_response_multi_term_joins_with_and() -> None:
    msg = get_year_response(GROVER_CLEVELAND, check_name_result=False, check_order_result=False)
    assert msg == "Wrong! The correct answer is president Grover Cleveland, order number 22 and 24."


# get_order_response

def test_get_order_response_correct() -> None:
    assert get_order_response(GEORGE_WASHINGTON, check_name_result=True, check_year_result=True) == "Correct!"


def test_get_order_response_both_wrong_message_singleton() -> None:
    msg = get_order_response(GEORGE_WASHINGTON, check_name_result=False, check_year_result=False)
    assert msg == "Wrong! The correct answer is president George Washington, start year 1789."


def test_get_order_response_only_year_wrong() -> None:
    msg = get_order_response(GEORGE_WASHINGTON, check_name_result=True, check_year_result=False)
    assert msg == "Wrong start year! The correct start year is 1789."


def test_get_order_response_only_name_wrong() -> None:
    msg = get_order_response(GEORGE_WASHINGTON, check_name_result=False, check_year_result=True)
    assert msg == "Wrong president! The correct president is George Washington."


def test_get_order_response_multi_term_joins_with_and() -> None:
    msg = get_order_response(GROVER_CLEVELAND, check_name_result=True, check_year_result=False)
    assert msg == "Wrong start year! The correct start year is 1885 and 1893."


# get_name_response

def test_get_name_response_correct() -> None:
    assert get_name_response(GEORGE_WASHINGTON, check_order_result=True, check_year_result=True) == "Correct!"


def test_get_name_response_both_wrong_message_singleton() -> None:
    msg = get_name_response(GEORGE_WASHINGTON, check_order_result=False, check_year_result=False)
    assert msg == "Wrong! The correct answer is order number 1, start year 1789."


def test_get_name_response_only_year_wrong() -> None:
    msg = get_name_response(GEORGE_WASHINGTON, check_order_result=True, check_year_result=False)
    assert msg == "Wrong start year! The correct start year is 1789."


def test_get_name_response_only_order_wrong() -> None:
    msg = get_name_response(GEORGE_WASHINGTON, check_order_result=False, check_year_result=True)
    assert msg == "Wrong order number! The correct order number is 1."


def test_get_name_response_multi_term_joins_with_and() -> None:
    msg = get_name_response(GROVER_CLEVELAND, check_order_result=False, check_year_result=False)
    assert msg == "Wrong! The correct answer is order number 22 and 24, start year 1885 and 1893."


# get_response

def test_get_response_routes_to_year() -> None:
    expected = get_year_response(GEORGE_WASHINGTON, check_name_result=True, check_order_result=False)
    routed = get_response(
        GEORGE_WASHINGTON, "year", check_name_result=True, check_order_result=False, check_year_result=None,
    )
    assert routed == expected


def test_get_response_routes_to_order() -> None:
    expected = get_order_response(GEORGE_WASHINGTON, check_name_result=False, check_year_result=True)
    routed = get_response(
        GEORGE_WASHINGTON, "order", check_name_result=False, check_order_result=None, check_year_result=True,
    )
    assert routed == expected


def test_get_response_routes_to_name() -> None:
    expected = get_name_response(GEORGE_WASHINGTON, check_order_result=True, check_year_result=False)
    routed = get_response(
        GEORGE_WASHINGTON, "name", check_name_result=None, check_order_result=True, check_year_result=False,
    )
    assert routed == expected


@pytest.mark.parametrize(
    ("qtype","kwargs","frag"),
    [
        ("year",  {"check_name_result": True}, "check_name_result and check_order_result"),
        ("order", {"check_name_result": True}, "check_name_result and check_year_result"),
        ("name",  {"check_order_result": True}, "check_order_result and check_year_result"),
    ],
)
def test_get_response_missing_required_args_raises(qtype: str, kwargs: dict[str, bool], frag: str) -> None:
    with pytest.raises(ValueError) as ei:  # noqa: PT011
        get_response(GEORGE_WASHINGTON, qtype, **kwargs)
    assert frag in str(ei.value)


def test_get_response_unknown_type_raises() -> None:
    with pytest.raises(ValueError) as ei:  # noqa: PT011
        get_response(GEORGE_WASHINGTON, "foobar", check_name_result=True, check_order_result=True, check_year_result=True)
    assert "Unknown question type: foobar" in str(ei.value)
