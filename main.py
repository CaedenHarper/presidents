import argparse
import logging
import random
import sys
from dataclasses import dataclass
from typing import ClassVar, Literal

from presidents import ALL_PRESIDENTS, NUM_PRESIDENTS, President
from quiz_statistics import QuizStatistics


class Settings:
    """Stores configuration settings for the quiz game.

    Attributes:
        VERBOSE_QUIET (Literal[0]): Verbose quiet magic number.
        VERBOSE_NORMAL (Literal[1]): Verbose normal magic number.
        VERBOSE_VERBOSE (Literal[2]): Verbose verbose magic number.
        repeat_questions (bool): If true, questions may be repeated before all have been asked.
        end_early (bool): If true, ends the game when all questions have been asked.
        president_range (tuple[int, int]): Range of presidents to include.
        verbose_level (int): Verbosity level.
        allow_ambiguity (bool): If true, ambiguous answers are allowed.
    """

    VERBOSE_QUIET = 0
    VERBOSE_NORMAL = 1
    VERBOSE_VERBOSE = 2

    def __init__(self,
                 *,
                 repeat_questions: bool = False,
                 end_early: bool = False,
                 president_range: tuple[int, int] | None = None,
                 verbose_level: int | None = None,
                 allow_ambiguity: bool = False) -> None:
        """Initialize Settings with configuration options."""
        self.repeat_questions = repeat_questions
        self.end_early = end_early
        self.president_range = (
            president_range
            if president_range is not None
            and 1 <= president_range[0] <= president_range[1] <= NUM_PRESIDENTS + 1
            else (1, NUM_PRESIDENTS + 1)
        )
        self.verbose_level = verbose_level if verbose_level in (0, 1, 2) else 1
        self.allow_ambiguity = allow_ambiguity

    def pretty_print(self) -> str:
        """Return a formatted string summarizing all settings for the quiz game.

        Returns:
            str: A string summarizing all configuration fields.
        """
        return (f"repeat_questions={self.repeat_questions}, "
                f"end_early={self.end_early}, "
                f"president_range={self.president_range}, "
                f"verbose_level={self.verbose_level}, "
                f"allow_ambiguity={self.allow_ambiguity}")

LOGGER = logging.getLogger(__name__)

GAME_STATS = QuizStatistics()
GAME_SETTINGS = Settings()

def format_as_percent(n: int, d: int) -> str:
    """Helper function to format a numerator and denominator as a percent to two decimal places."""
    return f"{(n / d * 100) if d > 0 else 0:.2f}%"

def get_year_response(president: President, *, check_name_result: bool, check_order_result: bool) -> str:
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

def get_order_response(president: President, *, check_name_result: bool, check_year_result: bool) -> str:
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

def get_name_response(president: President, *, check_order_result: bool, check_year_result: bool) -> str:
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

        return get_year_response(president, check_name_result=check_name_result, check_order_result=check_order_result)

    if question_type == "order":
        if check_name_result is None or check_year_result is None:
            msg = f"Both check_name_result and check_year_result must be provided for '{question_type}' question type."
            raise ValueError(msg)

        return get_order_response(president, check_name_result=check_name_result, check_year_result=check_year_result)

    if question_type == "name":
        if check_order_result is None or check_year_result is None:
            msg = f"Both check_order_result and check_year_result must be provided for '{question_type}' question type."
            raise ValueError(msg)

        return get_name_response(president, check_order_result=check_order_result, check_year_result=check_year_result)

    msg = "Unknown question type: " + question_type
    raise ValueError(msg)

def parse_arguments(settings: Settings) -> None:
    """Parse command line arguments into passed settings object."""
    # Type-hint parsed arguments (https://stackoverflow.com/questions/42279063/python-typehints-for-argparse-namespace-objects)
    @dataclass
    class ArgumentTypes:
        repeat: bool
        end_early: bool
        range: tuple[int, int]
        verbosity: Literal[0, 1, 2]
        allow_ambiguity: bool

    # TODO: add "sequential" option for going in order instead of random
    parser = argparse.ArgumentParser(description="Quiz game for US presidents.")
    # ensure -r and -e cant be used together
    repeat_group = parser.add_mutually_exclusive_group()
    repeat_group.add_argument("-r",
                              "--repeat",
                              action="store_true",
                              help=(
                                  "Allows repeat questions before all questions have been exhausted. "
                                  "Can not be used with --end-early. (Default: false)"
                              ))
    repeat_group.add_argument("-e",
                              "--end-early",
                              action="store_true",
                              help="Ends questions when all have been asked. Can not be used with --repeat. (Default: false)")
    parser.add_argument("-R",
                        "--range",
                        type=int,
                        nargs=2,
                        metavar=("START", "END"),
                        default=(1, NUM_PRESIDENTS),
                        help=f"Range of presidents to include, (1-{NUM_PRESIDENTS}). (Default: all)")
    parser.add_argument("-v",
                        "--verbosity",
                        type=int,
                        choices=[0, 1, 2],
                        default=1,
                        help="Verbosity level: 0 = quiet, 1 = normal, 2 = verbose. (Default: 1)")
    parser.add_argument("-a",
                        "--allow-ambiguity",
                        action="store_true",
                        help=(
                            "Allows amibguous answers. For example, 'John Adams' will count for both presidents if this flag is true. "
                            "(Default: false)"
                        ))

    args = ArgumentTypes(**parser.parse_args().__dict__)

    # Update settings based on parsed arguments
    settings.repeat_questions = args.repeat
    settings.end_early = args.end_early
    if 1 <= args.range[0] <= args.range[1] <= NUM_PRESIDENTS:
        settings.president_range = (args.range[0], args.range[1])
    else:
        parser.error(f"Invalid range: {args.range}. Must be between 1 and "
                     f"{NUM_PRESIDENTS}, inclusive, with START <= END.")
    settings.verbose_level = args.verbosity
    settings.allow_ambiguity = args.allow_ambiguity

    root = logging.getLogger()

    # TODO: move to logging setup function
    # Update logging level based on verbosity
    if settings.verbose_level == settings.VERBOSE_QUIET:
        root.setLevel(logging.ERROR)
    elif settings.verbose_level == settings.VERBOSE_VERBOSE:
        root.setLevel(logging.DEBUG)
    else: # settings.VERBOSE_NORMAL
        root.setLevel(logging.INFO)

    # Add a formatter that changes format based on severity
    class SeverityFormatter(logging.Formatter):
        FORMATS: ClassVar[dict[int, str]] = {
            logging.DEBUG: "[%(name)s:DEBUG] %(message)s",
            logging.INFO: "%(message)s",
            logging.WARNING: "[WARNING] %(message)s",
            logging.ERROR: "[ERROR] %(message)s",
            logging.CRITICAL: "[CRITICAL] %(message)s",
        }
        def format(self, record: logging.LogRecord) -> str:
            fmt = self.FORMATS.get(record.levelno, "%(message)s")
            self._style._fmt = fmt  # noqa: SLF001
            return super().format(record)

    handler = logging.StreamHandler()
    handler.setFormatter(SeverityFormatter())
    root.addHandler(handler)

def main() -> None:
    """Run the main game loop."""
    starting_presidents = ALL_PRESIDENTS[GAME_SETTINGS.president_range[0] - 1 : GAME_SETTINGS.president_range[1]]
    LOGGER.debug("Starting presidents: %s", [str(p) for p in starting_presidents])
    expected_length = GAME_SETTINGS.president_range[1] - GAME_SETTINGS.president_range[0] + 1
    if len(starting_presidents) != expected_length:
        LOGGER.error("President range does not match number of starting presidents. Expected length: %s from (%s, %s), got %s.",
                     expected_length, GAME_SETTINGS.president_range[0], GAME_SETTINGS.president_range[1], len(starting_presidents))
        sys.exit(1)

    remaining_presidents = starting_presidents.copy()

    while True:
        print(f"\nRound number {GAME_STATS.total_questions + 1}! (ctrl-c to quit)")
        # by default, don't repeat questions until all have been asked
        if len(remaining_presidents) == 0 and GAME_SETTINGS.end_early:
            print("All presidents have been asked! Ending...")
            raise KeyboardInterrupt

        if len(remaining_presidents) == 0:
            LOGGER.info("All presidents have been asked! Restarting...")
            remaining_presidents = starting_presidents.copy()

        if not GAME_SETTINGS.repeat_questions:
            LOGGER.debug("Remaining presidents: %s", [str(p) for p in remaining_presidents])
            current_president = random.choice(remaining_presidents)
            remaining_presidents.remove(current_president)
        else:
            current_president = random.choice(starting_presidents)

        # what information do we give the user?
        # not year if it is an ambiguous year
        question_type = random.choice(["name", "order"] if current_president.is_year_ambiguous() else ["year", "order", "name"])

        if question_type == "year":
            start_year_str = " and ".join(current_president.start_year)

            print(f"Year = {start_year_str}:")
            user_name = input("Who was the president? ")
            check_name_result = current_president.check_name(user_name, allow_ambiguity=GAME_SETTINGS.allow_ambiguity)
            user_order = input("What was the order number? (if multiple, separate with spaces) ")
            check_order_result = current_president.check_order(user_order)

            # TODO: move logging to function to allow reuse between question types
            LOGGER.debug("User input: name='%s', order='%s'", user_name, user_order)
            LOGGER.debug("Check results: name=%s, order=%s", check_name_result, check_order_result)
            LOGGER.debug("Before recording: %s", GAME_STATS.pretty_print())
            GAME_STATS.record_year_question(correct_name=check_name_result, correct_order=check_order_result)
            LOGGER.debug("After recording: %s", GAME_STATS.pretty_print())

            print(
                get_response(current_president,
                question_type,
                check_name_result=check_name_result,
                check_order_result=check_order_result,
                check_year_result=None),
                )
        elif question_type == "order":
            order_str = " and ".join(current_president.order_numbers)

            print(f"Order number = {order_str}:")
            user_name = input("Who was the president? ")
            check_name_result = current_president.check_name(user_name, allow_ambiguity=GAME_SETTINGS.allow_ambiguity)
            user_year = input("What year did they start their term? (if multiple, separate with spaces) ")
            check_year_result = current_president.check_year(user_year)

            LOGGER.debug("User input: name='%s', year='%s'", user_name, user_year)
            LOGGER.debug("Check results: name=%s, year=%s", check_name_result, check_year_result)
            LOGGER.debug("Before recording: %s", GAME_STATS.pretty_print())
            GAME_STATS.record_order_question(correct_name=check_name_result, correct_year=check_year_result)
            LOGGER.debug("After recording: %s", GAME_STATS.pretty_print())

            print(
                get_response(current_president,
                             question_type,
                             check_name_result=check_name_result,
                             check_order_result=None,
                             check_year_result=check_year_result),
                )
        elif question_type == "name":
            name_str = current_president.get_president_name()

            print(f"President = {name_str}:")
            user_order = input("What was their order number? (if multiple, separate with spaces) ")
            check_order_result = current_president.check_order(user_order)
            user_year = input("What year did they start their term? (if multiple, separate with spaces) ")
            check_year_result = current_president.check_year(user_year)

            LOGGER.debug("User input: order='%s', year='%s'", user_order, user_year)
            LOGGER.debug("Check results: order=%s, year=%s", check_order_result, check_year_result)
            LOGGER.debug("Before recording: %s", GAME_STATS.pretty_print())
            GAME_STATS.record_name_question(correct_order=check_order_result, correct_year=check_year_result)
            LOGGER.debug("After recording: %s", GAME_STATS.pretty_print())

            print(
                get_response(current_president,
                             question_type,
                             check_name_result=None,
                             check_order_result=check_order_result,
                             check_year_result=check_year_result),
                )

        else: # unexpected question type
            LOGGER.error("Unknown question type: %s", question_type)

if __name__ == "__main__":
    parse_arguments(GAME_SETTINGS)
    LOGGER.debug(GAME_SETTINGS.pretty_print())

    try:
        main()
    except KeyboardInterrupt:
        # TODO: move to a function
        print(f"""\n\nFinal statistics:

              Total questions: {GAME_STATS.total_questions}
              Correct questions: {GAME_STATS.correct_questions} """
              f"""({(GAME_STATS.correct_questions / GAME_STATS.total_questions * 100) if GAME_STATS.total_questions > 0 else 0:.2f}%)
              Half-correct questions: """
              f"""{GAME_STATS.half_correct_questions} ({format_as_percent(GAME_STATS.half_correct_questions, GAME_STATS.total_questions)})
              Correct names: {GAME_STATS.correct_names} ({format_as_percent(GAME_STATS.correct_names, GAME_STATS.name_questions)})
              Correct orders: {GAME_STATS.correct_orders} ({format_as_percent(GAME_STATS.correct_orders, GAME_STATS.order_questions)})
              Correct years: {GAME_STATS.correct_years} ({format_as_percent(GAME_STATS.correct_years, GAME_STATS.year_questions)})""")

        LOGGER.info("\nExiting...")
        sys.exit(1)
