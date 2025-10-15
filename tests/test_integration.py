import builtins
import random
import runpy
import sys
import typing

import pytest

# Helper functions to create mock input and random.choice functions with predetermined returns

def get_fake_input(_answers: list[str]) -> typing.Callable[[str], str]:
    answers = iter(_answers)
    def fake_input(_prompt: str="") -> str:
        return next(answers)
    return fake_input

# match random.choice type signature
_T = typing.TypeVar("_T")
def get_forced_choice(_forced_responses: list[str]) -> typing.Callable[[typing.Sequence[_T]], _T]:
    forced_responses = iter(_forced_responses)
    def forced_choice(seq: typing.Sequence[_T]) -> _T:
        # Force question type sequence; otherwise pick first item deterministically.
        if isinstance(seq, list) and set(seq) == {"year", "order", "name"}:
            try:
                return typing.cast("_T", next(forced_responses)) # tell the checker this is the same T
            except StopIteration:
                return seq[0]
        return seq[0]
    return forced_choice

@pytest.mark.usefixtures("capsys")
def test_e2e_year_question_single_round(capsys: pytest.CaptureFixture[str]) -> None:
    """Force a 'year' question for George Washington.

    Inputs:
      - name: 'George Washington'
      - order: '1'
    Expect:
      - Prints the year prompt, marks answer 'Correct!'
      - On next loop, end-early triggers and prints ending message
      - Final summary shows one total question, 1 correct, 1 half-correct,
        correct_names=1, correct_orders=1, correct_years=0.
    """
    original_choice = random.choice

    # mock functions
    forced_choice = get_forced_choice(["year"])
    fake_input = get_fake_input(["George Washington", "1"])

    argv_backup = sys.argv[:]
    sys.argv = ["main.py", "-R", "1", "1", "-e", "-v", "0"]

    builtins_input_backup = builtins.input
    try:
        random.choice = forced_choice
        builtins.input = fake_input

        with pytest.raises(SystemExit) as ei:
            runpy.run_module("main", run_name="__main__")
        assert ei.value.code == 1
    finally:
        random.choice = original_choice
        builtins.input = builtins_input_backup
        sys.argv = argv_backup

    out = capsys.readouterr()
    # Prompts and correctness
    assert "Round number 1!" in out.out
    assert "Year = 1789:" in out.out
    assert "Correct!" in out.out
    # End-early path
    assert "All presidents have been asked! Ending..." in out.out
    # Final stats summary (printed by the __main__ KeyboardInterrupt handler)
    assert "Final statistics:" in out.out
    assert "Total questions: 1" in out.out
    assert "Correct questions: 1" in out.out
    assert "Half-correct questions: 1" in out.out
    assert "Correct names: 1" in out.out
    assert "Correct orders: 1" in out.out
    # For a 'year' question, year stats are untouched
    assert "Correct years: 0" in out.out


@pytest.mark.usefixtures("capsys")
def test_e2e_order_question_single_round(capsys: pytest.CaptureFixture[str]) -> None:
    """Force an 'order' question for George Washington.

    Inputs:
      - name: 'George Washington'
      - start year: '1789'
    Expect:
      - order prompt displayed
      - final stats: name_questions=1, year_questions=1, both correct
    """
    original_choice = random.choice

    # mock functions
    forced_choice = get_forced_choice(["order"])
    fake_input = get_fake_input(["George Washington", "1789"])

    argv_backup = sys.argv[:]
    sys.argv = ["main.py", "-R", "1", "1", "-e", "-v", "0"]

    builtins_input_backup = builtins.input
    try:
        random.choice = forced_choice
        builtins.input = fake_input

        with pytest.raises(SystemExit) as ei:
            runpy.run_module("main", run_name="__main__")
        assert ei.value.code == 1
    finally:
        random.choice = original_choice
        builtins.input = builtins_input_backup
        sys.argv = argv_backup

    out = capsys.readouterr()
    assert "Order number = 1:" in out.out
    assert "Correct!" in out.out
    assert "Final statistics:" in out.out
    # Name + year paths touched for 'order' question
    assert "Correct names: 1" in out.out
    assert "Correct years: 1" in out.out


@pytest.mark.usefixtures("capsys")
def test_e2e_name_question_single_round(capsys: pytest.CaptureFixture[str]) -> None:
    """Force a 'name' question for George Washington.

    Inputs:
      - order: '1'
      - start year: '1789'
    Expect:
      - name prompt displayed with the full name given
      - final stats: order_questions=1, year_questions=1, both correct
    """
    original_choice = random.choice

    # mock functions
    forced_choice = get_forced_choice(["name"])
    fake_input = get_fake_input(["1", "1789"])

    argv_backup = sys.argv[:]
    sys.argv = ["main.py", "-R", "1", "1", "-e", "-v", "0"]

    builtins_input_backup = builtins.input
    try:
        random.choice = forced_choice
        builtins.input = fake_input

        with pytest.raises(SystemExit) as ei:
            runpy.run_module("main", run_name="__main__")
        assert ei.value.code == 1
    finally:
        random.choice = original_choice
        builtins.input = builtins_input_backup
        sys.argv = argv_backup

    out = capsys.readouterr()
    assert "President = George Washington:" in out.out
    assert "Correct!" in out.out
    assert "Final statistics:" in out.out
    # Order + year paths touched for 'name' question
    assert "Correct orders: 1" in out.out
    assert "Correct years: 1" in out.out

@pytest.mark.usefixtures("capsys")
def test_e2e_multiple_rounds(capsys: pytest.CaptureFixture[str]) -> None:
    """Run 5 deterministic rounds over the first five presidents with end-early.

    Forced question types per round:
      1: year   (Washington)
      2: order  (John Adams)
      3: name   (Jefferson)
      4: year   (Madison)
      5: order  (Monroe)
    All answers are correct; verify final stats.
    """
    original_choice = random.choice

    # mock functions
    forced_choice = get_forced_choice(["year", "order", "name", "year", "order"])
    fake_input = get_fake_input([
        # 1) Washington (year)
        "George Washington", "1",
        # 2) John Adams (order)
        "John Adams", "1797",
        # 3) Jefferson (name)
        "3", "1801",
        # 4) Madison (year)
        "James Madison", "4",
        # 5) Monroe (order)
        "James Monroe", "1817",
    ])

    argv_backup = sys.argv[:]
    sys.argv = ["main.py", "-R", "1", "5", "-e", "-v", "0"]
    builtins_input_backup = builtins.input
    try:
        random.choice = forced_choice
        builtins.input = fake_input

        with pytest.raises(SystemExit) as ei:
            runpy.run_module("main", run_name="__main__")
        assert ei.value.code == 1  # program exits via KeyboardInterrupt handler
    finally:
        random.choice = original_choice
        builtins.input = builtins_input_backup
        sys.argv = argv_backup

    out = capsys.readouterr()

    # Prompts for each round
    assert "Round number 1!" in out.out
    assert "Round number 5!" in out.out
    assert "Year = 1789:" in out.out                    # Washington
    assert "Order number = 2:" in out.out               # John Adams
    assert "President = Thomas Jefferson:" in out.out
    assert "Year = 1809:" in out.out                    # Madison
    assert "Order number = 5:" in out.out               # Monroe

    # All correct each round
    assert out.out.count("Correct!") == 5

    # End-early and final summary
    assert "All presidents have been asked! Ending..." in out.out
    assert "Final statistics:" in out.out
    assert "Total questions: 5" in out.out
    assert "Correct questions: 5" in out.out
    assert "Half-correct questions: 5" in out.out
    assert "Correct names: 4" in out.out     # rounds: year, order, order, year -> 4 name questions
    assert "Correct orders: 3" in out.out    # rounds: year, name, year -> 3 order questions
    assert "Correct years: 3" in out.out     # rounds: order, name, order -> 3 year questions

@pytest.mark.usefixtures("capsys")
def test_e2e_ambiguous_years_never_year_question(capsys: pytest.CaptureFixture[str]) -> None:
    """Ensure presidents with ambiguous start years (e.g., 1841) never get a 'year' question.

    We set the range to William Henry Harrison (9) and John Tyler (10), then force the
    question-type picker to try 'year'—the program should override to 'name'/'order'.
    """
    original_choice = random.choice

    # this method requires a specific, different forced_choice
    def forced_choice(seq: typing.Sequence[_T]) -> _T:
        # This should never happen in this test case
        if isinstance(seq, list) and set(seq) == {"year", "order", "name"}:
            msg = "Year question type unexpectedly possible."
            raise AssertionError(msg)
        # When the program detects an ambiguous year, it re-picks from ['name','order'].
        # Return 'name' deterministically so inputs are simple (order, year).
        if isinstance(seq, list) and set(seq) == {"name", "order"}:
            return typing.cast("_T", "name") # cast for type checker
        # For presidents/other sequences, pick the first element to keep things deterministic.
        return seq[0]

    fake_input = get_fake_input(["9", "1841", "10", "1841"])

    argv_backup = sys.argv[:]
    sys.argv = ["main.py", "-R", "9", "10", "-e", "-v", "0"]
    builtins_input_backup = builtins.input
    try:
        random.choice = forced_choice
        builtins.input = fake_input

        with pytest.raises(SystemExit) as ei:
            runpy.run_module("main", run_name="__main__")
        assert ei.value.code == 1
    finally:
        random.choice = original_choice
        builtins.input = builtins_input_backup
        sys.argv = argv_backup

    out = capsys.readouterr()
    # We should see two rounds and 'name' prompts for both presidents
    assert "Round number 1!" in out.out
    assert "Round number 2!" in out.out
    assert "President = William Henry Harrison:" in out.out
    assert "President = John Tyler:" in out.out

    # Critically: no 'Year =' prompt should appear at all for ambiguous-year presidents
    assert "Year = " not in out.out
    assert "Year = 1841:" not in out.out

    # Sanity: both were answered correctly
    assert out.out.count("Correct!") == 2

    # End-early + final summary present
    assert "All presidents have been asked! Ending..." in out.out
    assert "Final statistics:" in out.out
