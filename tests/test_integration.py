import builtins
import importlib
import logging
import random
import runpy
import sys
import typing

import pytest

# Helper functions to create mock input and random.choice functions with predetermined returns

def get_fake_input(_answers: list[str], *, raise_keyboard_after: int | None = None) -> typing.Callable[[str], str]:
    """Return an input() replacement that yields from `_answers`.

    If `raise_keyboard_after` is provided, raise KeyboardInterrupt after that many total calls.
    """
    answers = iter(_answers)
    count = 0
    def _fake_input(_prompt: str="") -> str:
        nonlocal count
        count += 1
        if raise_keyboard_after is not None and count > raise_keyboard_after:
            raise KeyboardInterrupt

        return next(answers)
    return _fake_input

# match random.choice type signature
_T = typing.TypeVar("_T")
def get_forced_choice(_forced_qtypes: list[str]) -> typing.Callable[[typing.Sequence[_T]], _T]:
    forced_qtypes = iter(_forced_qtypes)
    def forced_choice(seq: typing.Sequence[_T]) -> _T:
        # Force question type sequence; otherwise pick first item deterministically.
        if isinstance(seq, list) and set(seq) == {"year", "order", "name"}:
                return typing.cast("_T", next(forced_qtypes)) # tell the type checker this is the same T
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

def run_quiz(forced_qtypes: list[str],
             inputs: list[str],
             argv: list[str],
             choice_override: typing.Callable[[typing.Sequence[_T]], _T] | None = None,
             input_override: typing.Callable[[str], str] | None = None) -> int:
    """Run the quiz package as if via `python -m presidents_quiz`.

      - forced question types (or a complete choice function override),
      - scripted user inputs (or a complete input function override),
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

    random.choice = choice_override or get_forced_choice(forced_qtypes)
    builtins.input = input_override or get_fake_input(inputs)
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

# misc tests

def test_random_choice_called_on_starting_presidents(capsys: pytest.CaptureFixture[str]) -> None:
    """Ensure the line: current_president = random.choice(starting_presidents) is exercised.

    Detects a call where seq contains President objects.
    """
    saw_president_seq = {"called": False}

    def choice_with_probe(seq: typing.Sequence[_T]) -> _T:
        # Detect a list of President-ish objects (duck-type by attribute).
        if isinstance(seq, list) and seq and hasattr(seq[0], "get_president_name"):
            saw_president_seq["called"] = True
        # For the question-type selection, force 'name' to keep inputs simple.
        if isinstance(seq, list) and set(seq) == {"year", "order", "name"}:
            return typing.cast("_T", "name")
        return seq[0]

    code = run_quiz(
        forced_qtypes=[],  # ignored because we provide a full override
        inputs=["1", "1789"],  # order + year for the 'name' question
        argv=["-R", "1", "1", "-e", "-v", "0"],
        choice_override=choice_with_probe,
    )
    assert code == 1
    assert saw_president_seq["called"] is True

    out = capsys.readouterr().out
    assert "President = George Washington:" in out
    assert "Correct!" in out


def test_restart_when_remaining_presidents_empty_logs_and_restarts(caplog: pytest.LogCaptureFixture) -> None:
    """Cover restart with remaining presidents empty branch.

    Runs with a single-president range and end_early=False, then
    performs two rounds and exits via KeyboardInterrupt.
    """
    # Capture INFO logs from the root (parse_arguments installs the handler)
    caplog.set_level(logging.INFO)

    # Custom input: 2 rounds of 'name' questions, then KeyboardInterrupt to stop.
    fake_input = get_fake_input(["1", "1789", "1", "1789"], raise_keyboard_after=4)

    # Choice override to (a) detect President list call and (b) force 'name' for Q-type
    def choice_override(seq: typing.Sequence[_T]) -> _T:
        if isinstance(seq, list) and set(seq) == {"year", "order", "name"}:
            return typing.cast("_T", "name")
        return seq[0]

    # Patch bits manually to use our custom fake_input
    _reset_game_state()
    original_choice = random.choice
    original_input = builtins.input
    argv_backup = sys.argv[:]
    try:
        random.choice = choice_override
        builtins.input = fake_input
        sys.argv = ["presidents_quiz", "-R", "1", "1"]

        with pytest.raises(SystemExit) as ei:
            runpy.run_module("presidents_quiz", run_name="__main__")
        assert int(ei.value.code if ei.value.code is not None else -1) == 1
    finally:
        random.choice = original_choice
        builtins.input = original_input
        sys.argv = argv_backup

    # Assert the restart log happened at least once
    text = caplog.text
    assert "All presidents have been asked! Restarting..." in text

def test_expected_length_mismatch_exits_with_error(caplog: pytest.LogCaptureFixture) -> None:
    """Cover presidents length mismatch error.

    We bypass parse_arguments and set an impossible range to force the mismatch.
    """
    caplog.set_level(logging.ERROR)

    import presidents_quiz.main as m  # noqa: PLC0415
    _reset_game_state()
    # Force an impossible range so expected_length >> available slice length
    m.GAME_SETTINGS.president_range = (1, 1000)

    with pytest.raises(SystemExit) as ei:
        m.main()
    assert int(ei.value.code if ei.value.code is not None else -1) == 1

    assert "President range does not match number of starting presidents." in caplog.text

def test_selection_uses_remaining_list_when_no_repeat(capsys: pytest.CaptureFixture[str]) -> None:
    """Cover the non-repeat branch in main().

    Expect our choice override to see a presidents sequence of length 2 (round 1),
    then length 1 (round 2), proving removal happened.
    """
    _reset_game_state()

    president_seq_lengths: list[int] = []

    def choice_override(seq: typing.Sequence[_T]) -> _T:
        # Record only when we're picking a president
        if isinstance(seq, list) and seq and hasattr(seq[0], "get_president_name"):
            president_seq_lengths.append(len(seq))
            return seq[0]  # deterministic: pick first
        # For question-type, always ask 'name' so inputs are simple
        if isinstance(seq, list) and set(seq) == {"year", "order", "name"}:
            return typing.cast("_T", "name")
        return seq[0]

    # Two rounds, end-early=True, so the run finishes on its own after 2 questions
    original_choice = random.choice
    original_input = builtins.input
    argv_backup = sys.argv[:]
    try:
        random.choice = choice_override
        builtins.input = get_fake_input([
            # Round 1 (George Washington): order + year
            "1", "1789",
            # Round 2 (John Adams): order + year
            "2", "1797",
        ])
        sys.argv = ["presidents_quiz", "-R", "1", "2", "-e", "-v", "0"]

        with pytest.raises(SystemExit) as ei:
            runpy.run_module("presidents_quiz", run_name="__main__")
        assert int(ei.value.code if ei.value.code is not None else -1) == 1
    finally:
        random.choice = original_choice
        builtins.input = original_input
        sys.argv = argv_backup

    # We should have picked from remaining_presidents (2 items), then from it again after removal (1 item)
    assert president_seq_lengths == [2, 1]

    out = capsys.readouterr().out
    assert "Round number 1!" in out
    assert "Round number 2!" in out
    assert "President = George Washington:" in out
    assert "President = John Adams:" in out


def test_selection_uses_starting_list_when_repeat_enabled(capsys: pytest.CaptureFixture[str]) -> None:
    """Cover the repeat branch in main().

    Expect our choice override to see a presidents sequence of length 2 on *both* rounds,
    proving it keeps choosing from starting_presidents (no removal).
    """
    _reset_game_state()

    president_seq_lengths: list[int] = []

    def choice_override(seq: typing.Sequence[_T]) -> _T:
        if isinstance(seq, list) and seq and hasattr(seq[0], "get_president_name"):
            president_seq_lengths.append(len(seq))
            return seq[0]  # deterministic: pick first (likely Washington both rounds)
        if isinstance(seq, list) and set(seq) == {"year", "order", "name"}:
            return typing.cast("_T", "name")
        return seq[0]

    # Two rounds, repeat enabled; use a KeyboardInterrupt after 4 inputs to stop the loop
    original_choice = random.choice
    original_input = builtins.input
    argv_backup = sys.argv[:]
    try:
        random.choice = choice_override
        builtins.input = get_fake_input(
            ["1", "1789", "1", "1789"],  # two 'name' rounds: order + year each
            raise_keyboard_after=4,
        )
        sys.argv = ["presidents_quiz", "-R", "1", "2", "-r", "-v", "0"]

        with pytest.raises(SystemExit) as ei:
            runpy.run_module("presidents_quiz", run_name="__main__")
        assert int(ei.value.code if ei.value.code is not None else -1) == 1
    finally:
        random.choice = original_choice
        builtins.input = original_input
        sys.argv = argv_backup

    # Both rounds saw a 2-item president list -> selection came from starting_presidents
    assert all(x == 2 for x in president_seq_lengths)

    out = capsys.readouterr().out
    assert "Round number 1!" in out
    assert "Round number 2!" in out
    # Deterministic first pick both times
    assert out.count("President = George Washington:") >= 1

# test cli()

def test_cli_direct_invocation_prints_help_and_exits_with_stats(capsys: pytest.CaptureFixture[str]) -> None:
    """Directly call cli().

    - parse_arguments() runs (via cli())
    - main() runs one round and raises KeyboardInterrupt via -e path
    - cli() catches it, prints final stats, and exits with code 1
    """
    _reset_game_state()
    import presidents_quiz.main as m  # noqa: PLC0415

    # Patch globals
    original_choice = random.choice
    original_input = builtins.input
    argv_backup = sys.argv[:]

    try:
        random.choice = get_forced_choice(["name"])
        builtins.input = get_fake_input(["1", "1789"])
        sys.argv = ["presidents_quiz", "-R", "1", "1", "-e", "-v", "0"]

        with pytest.raises(SystemExit) as ei:
            m.cli()
        assert int(ei.value.code if ei.value.code is not None else -1) == 1
    finally:
        random.choice = original_choice
        builtins.input = original_input
        sys.argv = argv_backup

    out = capsys.readouterr().out
    # We hit the name path for Washington and printed final stats
    assert "President = George Washington:" in out
    assert "Correct!" in out
    assert "Final statistics:" in out
    assert "Total questions: 1" in out
