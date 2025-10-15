import builtins
import importlib
import logging
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
def get_forced_choice(_forced_qtypes: list[str]) -> typing.Callable[[typing.Sequence[_T]], _T]:
    forced_qtypes = iter(_forced_qtypes)
    def forced_choice(seq: typing.Sequence[_T]) -> _T:
        # Force question type sequence; otherwise pick first item deterministically.
        if isinstance(seq, list) and set(seq) == {"year", "order", "name"}:
            try:
                return typing.cast("_T", next(forced_qtypes)) # tell the type checker this is the same T
            except StopIteration:
                return seq[0]
        return seq[0]
    return forced_choice

def _reset_root_logger() -> None:
    """Avoid accumulating duplicate handlers across runs."""
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.NOTSET)


def _reset_game_state() -> None:
    """Reset module-level singletons in presidents_quiz.main so each test starts fresh."""
    # Import (or re-import) the modules we need
    import presidents_quiz.main as m  # noqa: PLC0415
    import presidents_quiz.quiz_settings as qs  # noqa: PLC0415
    import presidents_quiz.quiz_statistics as qst  # noqa: PLC0415

    importlib.reload(qs)
    importlib.reload(qst)
    # If main hangs on class objects, reload it too so it sees the fresh classes.
    importlib.reload(m)

    # Recreate the singletons that main uses
    m.GAME_SETTINGS = qs.QuizSettings()
    m.GAME_STATS = qst.QuizStatistics()

def run_quiz(forced_qtypes: list[str], inputs: list[str], argv: list[str]) -> int:
    """Run the quiz package as if via `python -m presidents_quiz`.

      - forced question types (for the 3-option selection),
      - scripted user inputs,
      - argv (e.g., ["-R","1","1","-e","-v","0"]).
    Returns the SystemExit code raised by the app.
    """
    # ensure clean slate
    _reset_game_state()
    _reset_root_logger()

    # set up patches
    original_choice = random.choice
    original_input = builtins.input
    argv_backup = sys.argv[:]

    random.choice = get_forced_choice(forced_qtypes)
    builtins.input = get_fake_input(inputs)
    sys.argv = ["presidents_quiz", *argv]   # what parse_arguments() will see

    try:
        with pytest.raises(SystemExit) as ei:
            # Execute the package entrypoint (src/presidents_quiz/__main__.py)
            runpy.run_module("presidents_quiz", run_name="__main__")
        return int(ei.value.code if ei.value.code is not None else -1)
    finally:
        # restore globals no matter what
        random.choice = original_choice
        builtins.input = original_input
        sys.argv = argv_backup


# integration tests

def test_e2e_year_question_single_round(capsys: pytest.CaptureFixture[str]) -> None:
    """Force a 'year' round for George Washington and end after one round."""
    code = run_quiz(
        forced_qtypes=["year"],
        inputs=["George Washington", "1"],
        argv=["-R", "1", "1", "-e", "-v", "0"],
    )
    assert code == 1

    out = capsys.readouterr().out
    assert "Round number 1!" in out
    assert "Year = 1789:" in out
    assert "Correct!" in out
    assert "All presidents have been asked! Ending..." in out
    assert "Final statistics:" in out
    assert "Total questions: 1" in out
    assert "Correct questions: 1" in out
    assert "Half-correct questions: 1" in out
    assert "Correct names: 1" in out
    assert "Correct orders: 1" in out
    assert "Correct years: 0" in out  # year-path doesn't increment year correctness


def test_e2e_order_question_single_round(capsys: pytest.CaptureFixture[str]) -> None:
    """Force an 'order' round for George Washington and end after one round."""
    code = run_quiz(
        forced_qtypes=["order"],
        inputs=["George Washington", "1789"],
        argv=["-R", "1", "1", "-e", "-v", "0"],
    )
    assert code == 1

    out = capsys.readouterr().out
    assert "Order number = 1:" in out
    assert "Correct!" in out
    assert "Final statistics:" in out
    assert "Correct names: 1" in out
    assert "Correct years: 1" in out


def test_e2e_name_question_single_round(capsys: pytest.CaptureFixture[str]) -> None:
    """Force a 'name' round for George Washington and end after one round."""
    code = run_quiz(
        forced_qtypes=["name"],
        inputs=["1", "1789"],
        argv=["-R", "1", "1", "-e", "-v", "0"],
    )
    assert code == 1

    out = capsys.readouterr().out
    assert "President = George Washington:" in out
    assert "Correct!" in out
    assert "Final statistics:" in out
    assert "Correct orders: 1" in out
    assert "Correct years: 1" in out


def test_e2e_multiple_rounds(capsys: pytest.CaptureFixture[str]) -> None:
    """Run 5 deterministic rounds over the first five presidents with end-early.

    Q types: year, order, name, year, order.
    """
    code = run_quiz(
        forced_qtypes=["year", "order", "name", "year", "order"],
        inputs=[
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
        ],
        argv=["-R", "1", "5", "-e", "-v", "0"],
    )
    assert code == 1

    out = capsys.readouterr().out
    assert "Round number 1!" in out
    assert "Round number 5!" in out
    assert "Year = 1789:" in out
    assert "Order number = 2:" in out
    assert "President = Thomas Jefferson:" in out
    assert "Year = 1809:" in out
    assert "Order number = 5:" in out
    assert out.count("Correct!") == 5
    assert "All presidents have been asked! Ending..." in out
    assert "Final statistics:" in out
    assert "Total questions: 5" in out
    assert "Correct questions: 5" in out
    assert "Half-correct questions: 5" in out
    assert "Correct names: 4" in out
    assert "Correct orders: 3" in out
    assert "Correct years: 3" in out


def test_e2e_ambiguous_years_never_year_question(capsys: pytest.CaptureFixture[str]) -> None:
    """For 1841 presidents (W. H. Harrison #9, John Tyler #10), year questions must not be asked.

    The game internally chooses from ['name','order'] for ambiguous years; our forced_choice
    returns seq[0], which is 'name' in that list.
    """
    code = run_quiz(
        forced_qtypes=[],
        inputs=[
            "9", "1841",
            "10", "1841",
        ],
        argv=["-R", "9", "10", "-e", "-v", "0"],
    )
    assert code == 1

    out = capsys.readouterr().out
    assert "Round number 1!" in out
    assert "Round number 2!" in out
    assert "President = William Henry Harrison:" in out
    assert "President = John Tyler:" in out
    assert "Year = " not in out
    assert out.count("Correct!") == 2
    assert "All presidents have been asked! Ending..." in out
    assert "Final statistics:" in out
