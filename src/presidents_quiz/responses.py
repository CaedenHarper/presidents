from presidents_quiz.presidents import President  # noqa: TC001 breaks 3.10 - 3.13

__all__ = ["get_response"]

def _get_year_response(president: President, *, check_name_result: bool, check_order_result: bool) -> str:
    """Return response based on which parts were correct in year response."""
    if check_name_result and check_order_result:
        return "Correct!"

    if not check_order_result and not check_name_result:
        return (
            f"Wrong! The correct answer is president {president}, "
            f"order number {' and '.join(president.order_numbers)}."
        )

    if not check_order_result:
        return (
            f"Wrong order number! The correct order number is "
            f"{' and '.join(president.order_numbers)}."
        )

    if not check_name_result:
        return f"Wrong president! The correct president is {president}."

    # should not be possible
    msg = "Unexpected combination of results."
    raise RuntimeError(msg)

def _get_order_response(president: President, *, check_name_result: bool, check_year_result: bool) -> str:
    """Return response based on which parts were correct in order response."""
    if check_name_result and check_year_result:
        return "Correct!"

    if not check_year_result and not check_name_result:
        return (
            f"Wrong! The correct answer is president {president}, "
            f"start year {' and '.join(president.start_year)}."
        )

    if not check_year_result:
        return (
            f"Wrong start year! The correct start year is "
            f"{' and '.join(president.start_year)}."
        )

    if not check_name_result:
        return f"Wrong president! The correct president is {president}."

    # should not be possible
    msg = "Unexpected combination of results."
    raise RuntimeError(msg)

def _get_name_response(president: President, *, check_order_result: bool, check_year_result: bool) -> str:
    """Return response based on which parts were correct in name response."""
    if check_order_result and check_year_result:
        return "Correct!"

    if not check_year_result and not check_order_result:
        return (
            f"Wrong! The correct answer is order number "
            f"{' and '.join(president.order_numbers)}, "
            f"start year {' and '.join(president.start_year)}."
        )

    if not check_year_result:
        return (
            f"Wrong start year! The correct start year is "
            f"{' and '.join(president.start_year)}."
        )

    if not check_order_result:
        return (
            f"Wrong order number! The correct order number is "
            f"{' and '.join(president.order_numbers)}."
        )

    # should not be possible
    msg = "Unexpected combination of results."
    raise RuntimeError(msg)

def get_response(president: President,
                 question_type: str,
                 *,
                 check_name_result: bool | None = None,
                 check_order_result: bool | None = None,
                 check_year_result: bool | None = None) -> str:
    """Return appropriate response based on which parts were correct."""
    if question_type == "year":
        if check_name_result is None or check_order_result is None:
            msg = f"Both check_name_result and check_order_result must be provided for '{question_type}' question type."
            raise ValueError(msg)

        return _get_year_response(president, check_name_result=check_name_result, check_order_result=check_order_result)

    if question_type == "order":
        if check_name_result is None or check_year_result is None:
            msg = f"Both check_name_result and check_year_result must be provided for '{question_type}' question type."
            raise ValueError(msg)

        return _get_order_response(president, check_name_result=check_name_result, check_year_result=check_year_result)

    if question_type == "name":
        if check_order_result is None or check_year_result is None:
            msg = f"Both check_order_result and check_year_result must be provided for '{question_type}' question type."
            raise ValueError(msg)

        return _get_name_response(president, check_order_result=check_order_result, check_year_result=check_year_result)

    msg = "Unknown question type: " + question_type
    raise ValueError(msg)
