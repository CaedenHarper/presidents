import logging
import sys
import typing

import pytest

from main import QuizSettings, parse_arguments
from presidents import NUM_PRESIDENTS

root = logging.getLogger()

@pytest.fixture(autouse=True)
def reset_logger() -> typing.Generator[None, None, None]:  # noqa: UP043 3.10 - 3.12 require all three type arguments
    """Keep root logger isolated per test: clear handlers and reset level."""
    logger = root
    old_handlers = list(logger.handlers)
    old_level = logger.level
    logger.handlers = []
    logger.setLevel(logging.NOTSET)
    yield
    logger.handlers = []
    logger.setLevel(old_level)
    # restore prior handlers if any (probably none for this module)
    for h in old_handlers:
        logger.addHandler(h)

def run_parse(args: list[str]) -> QuizSettings:
    """Run parse_arguments with a temporary sys.argv.

    Returns the settings object that was mutated.
    """
    settings = QuizSettings()
    argv_backup = sys.argv[:]
    try:
        sys.argv = ["prog", *args]
        parse_arguments(settings)
        return settings
    finally:
        sys.argv = argv_backup


# defaults

def test_defaults_update_settings_and_logger_installed() -> None:
    s = run_parse([])
    assert s.repeat_questions is False
    assert s.end_early is False
    # Default CLI range is (1, NUM_PRESIDENTS)
    assert s.president_range == (1, NUM_PRESIDENTS)
    assert s.verbose_level == QuizSettings.VERBOSE_NORMAL  # 1
    assert s.allow_ambiguity is False

    # One handler with the custom SeverityFormatter should be attached
    handlers = [h for h in root.handlers if h.formatter.__class__.__name__ == "SeverityFormatter"]
    assert len(handlers) == 1

    # Default verbosity -> INFO level
    assert root.level == logging.INFO


# -r and -e flags

def test_repeat_flag_sets_repeat_true() -> None:
    s = run_parse(["-r"])
    assert s.repeat_questions is True
    assert s.end_early is False


def test_end_early_flag_sets_end_early_true() -> None:
    s = run_parse(["-e"])
    assert s.end_early is True
    assert s.repeat_questions is False


def test_r_and_e_together_errors(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as ei:
        run_parse(["-r", "-e"])
    assert ei.value.code == 2
    err = capsys.readouterr().err
    # argparse wording for mutex groups
    assert "not allowed with argument" in err


# ranges

def test_valid_range_is_applied() -> None:
    s = run_parse(["-R", "3", "7"])
    assert s.president_range == (3, 7)


@pytest.mark.parametrize(("start","end"), [("5", "3"), ("0", "3"), ("1", str(NUM_PRESIDENTS + 1))])
def test_invalid_range_triggers_parser_error(start: str, end: str, capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as ei:
        run_parse(["-R", start, end])
    assert ei.value.code == 2
    err = capsys.readouterr().err
    assert "Invalid range:" in err
    assert "Must be between 1 and" in err


# verbosity and logging behavior

@pytest.mark.parametrize(
    ("level_arg", "expected_level"),
    [
        ("0", logging.ERROR),
        ("1", logging.INFO),
        ("2", logging.DEBUG),
    ],
)
def test_verbosity_sets_logger_level(level_arg: str, expected_level: int) -> None:
    run_parse(["-v", level_arg])
    assert root.level == expected_level


def test_severity_formatter_output_for_verbose_debug(capsys: pytest.CaptureFixture[str]) -> None:
    # -v 2 installs DEBUG and the custom formatter
    run_parse(["-v", "2"])

    root.debug("dmsg")
    root.info("imsg")
    root.warning("wmsg")
    root.error("emsg")

    out = capsys.readouterr().err  # StreamHandler uses stderr by default
    outlines = out.split("\n")
    # Expect the specific prefixes configured by SeverityFormatter
    assert "[root:DEBUG] dmsg" in outlines
    assert "imsg" in outlines # INFO should not have prefix
    assert "[WARNING] wmsg" in outlines
    assert "[ERROR] emsg" in outlines


def test_verbosity_info_filters_debug_and_formats(capsys: pytest.CaptureFixture[str]) -> None:
    run_parse(["-v", "1"])
    root.debug("should_not_show")
    root.info("hello_info")
    root.warning("hello_warn")

    out = capsys.readouterr().err
    assert "should_not_show" not in out
    assert "hello_info" in out
    assert "[WARNING] hello_warn" in out


def test_invalid_verbosity_choice_errors(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as ei:
        run_parse(["-v", "3"])
    assert ei.value.code == 2
    err = capsys.readouterr().err
    assert "invalid choice" in err.lower()

# -a flag

def test_ambiguous_flag_set_true() -> None:
    s = run_parse(["-a"])
    assert s.allow_ambiguity is True

def test_ambiguous_flag_set_false() -> None:
    s = run_parse([])
    assert s.allow_ambiguity is False
