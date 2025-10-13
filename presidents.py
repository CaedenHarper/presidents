import argparse
import logging
import random
import sys
from dataclasses import dataclass
from typing import ClassVar, Literal


class President:
    """Represents a U.S. president with name details, order numbers, and start years.

    Attributes:
        AMBIGIOUS_FULL_NAMES (list[str]): Full names requiring disambiguation.
        HALF_AMBIGIOUS_FULL_NAMES (list[str]): Full names ambiguous without middle name.
        AMBIGIOUS_LAST_NAMES (list[str]): Last names shared by multiple presidents.
        first_name (str): President's first name.
        last_name (str): President's last name.
        middle_name (str | None): Middle name or initial, if any.
        nickname (str | None): Nickname, if any.
        order_numbers (list[str]): Presidential order numbers.
        start_year (list[str]): Years presidency started.
    """
    # lists of ambigious names in lowercase
    # both george bushes require middle initials to disambiguate
    AMBIGIOUS_FULL_NAMES = ("george bush",)
    # currently only john adams is half-ambiguous, meaning if no middle name is given,
    # it's 1979 adams
    HALF_AMBIGIOUS_FULL_NAMES = ("john adams",)
    AMBIGIOUS_LAST_NAMES = ("adams", "bush", "roosevelt", "johnson", "harrison")
    # died first year in office
    AMBIGIOUS_YEARS = ("1841", "1881")
    def __init__(self,
                 first_name: str,
                 last_name: str,
                 order_numbers: list[str],
                 start_year: list[str],
                 *,
                 middle_name: str | None = None,
                 nickname: str | None = None) -> None:
        """Initialize a President instance.

        Args:
            first_name (str): President's first name.
            last_name (str): President's last name.
            order_numbers (list[str]): Presidential order numbers.
            start_year (list[str]): Years presidency started.
            middle_name (str, optional): Middle name or initial. Defaults to None.
            nickname (str, optional): Nickname. Defaults to None.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.order_numbers = order_numbers
        self.start_year = start_year
        self.middle_name = middle_name
        self.nickname = nickname

    def __str__(self) -> str:
        """Return a string representation of the president."""
        return self.get_president_name()

    def get_president_name(self) -> str:
        """Return the full name of the president."""
        if self.middle_name is not None:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    def is_full_name_ambiguous(self) -> bool:
        """Check if the president's full name is ambiguous.

        Returns:
            bool: True if the full name is ambiguous, False otherwise.
        """
        return self.first_name.lower() + " " + self.last_name.lower() \
            in self.AMBIGIOUS_FULL_NAMES

    def is_last_name_ambiguous(self) -> bool:
        """Check if the president's last name is ambiguous.

        Returns:
            bool: True if the last name is ambiguous, False otherwise.
        """
        return self.last_name.lower() in self.AMBIGIOUS_LAST_NAMES

    def is_year_ambiguous(self) -> bool:
        """Check if the president's start year is ambiguous.

        Returns:
            bool: True if the start year is ambiguous, False otherwise.
        """
        return any(year in self.AMBIGIOUS_YEARS for year in self.start_year)

class Statistics:
    """Tracks statistics for the quiz game.

    Attributes:
        total_questions (int): Total number of questions asked.
        correct_questions (int): Number of questions answered completely correctly.
        half_correct_questions (int): Number of questions answered partially correctly.
        correct_names (int): Number of times the name was answered correctly.
        name_questions (int): Number of questions where name was asked.
        correct_orders (int): Number of times the order number was answered correctly.
        order_questions (int): Number of questions where questions was asked.
        correct_years (int): Number of times the start year was answered correctly.
        year_questions (int): Number of questions where start year was asked.
    """
    def __init__(self) -> None:
        """Initialize all statistics counters to zero."""
        self.total_questions = 0
        self.correct_questions = 0
        self.half_correct_questions = 0

        self.correct_names = 0
        self.name_questions = 0

        self.correct_orders = 0
        self.order_questions = 0

        self.correct_years = 0
        self.year_questions = 0

    def record_year_question(self, *, correct_name: bool, correct_order: bool) -> None:
        """Record statistics for a 'year' type question.

        Args:
            correct_name (bool): Whether the president's name was answered correctly.
            correct_order (bool): Whether the order number was answered correctly.
        """
        self.total_questions += 1
        self.name_questions += 1
        self.order_questions += 1

        if correct_name and correct_order:
            self.correct_questions += 1

        if correct_name or correct_order:
            self.half_correct_questions += 1

        if correct_name:
            self.correct_names += 1

        if correct_order:
            self.correct_orders += 1

    def record_order_question(self, *, correct_name: bool, correct_year: bool) -> None:
        """Record statistics for an 'order' type question.

        Args:
            correct_name (bool): Whether the president's name was answered correctly.
            correct_year (bool): Whether the start year was answered correctly.
        """
        self.total_questions += 1
        self.name_questions += 1
        self.year_questions += 1

        if correct_name and correct_year:
            self.correct_questions += 1

        if correct_name or correct_year:
            self.half_correct_questions += 1

        if correct_name:
            self.correct_names += 1

        if correct_year:
            self.correct_years += 1

    def record_name_question(self, *, correct_order: bool, correct_year: bool) -> None:
        """Record statistics for a 'name' type question.

        Args:
            correct_order (bool): Whether the order number was answered correctly.
            correct_year (bool): Whether the start year was answered correctly.
        """
        self.total_questions += 1
        self.order_questions += 1
        self.year_questions += 1

        if correct_order and correct_year:
            self.correct_questions += 1

        if correct_order or correct_year:
            self.half_correct_questions += 1

        if correct_order:
            self.correct_orders += 1

        if correct_year:
            self.correct_years += 1

    def pretty_print(self) -> str:
        """Return a formatted string summarizing all statistics for the quiz game.

        This includes total questions, correct and half-correct answers, and
        breakdowns for names, orders, and years.

        Returns:
            str: A string summarizing all statistics fields.
        """
        return (f"total_questions={GAME_STATS.total_questions}, "
                f"correct_questions={GAME_STATS.correct_questions}, "
                f"half_correct_questions={GAME_STATS.half_correct_questions}, "
                f"correct_names={GAME_STATS.correct_names}, "
                f"name_questions={GAME_STATS.name_questions}, "
                f"correct_orders={GAME_STATS.correct_orders}, "
                f"order_questions={GAME_STATS.order_questions}, "
                f"correct_years={GAME_STATS.correct_years}, "
                f"year_questions={GAME_STATS.year_questions}")

class Settings:
    """Stores configuration settings for the quiz game.

    Attributes:
        repeat_questions (bool): If true, questions may be repeated
            before all have been asked.
        end_early (bool): If true, ends the game when all questions have been asked.
        president_range (tuple[int, int]): Range of presidents to include\
            (1-indexed, inclusive).
        verbose_level (Literal[0, 1, 2]): Verbosity level
            (0 = quiet, 1 = normal, 2 = verbose).
    """

    VERBOSE_QUIET = 0
    VERBOSE_NORMAL = 1
    VERBOSE_VERBOSE = 2

    def __init__(self,
                 *,
                 repeat_questions: bool = False,
                 end_early: bool = False,
                 president_range: tuple[int, int] | None = None,
                 verbose_level: Literal[0, 1, 2] | None = None) -> None:
        """Initialize Settings with configuration options.

        Args:
            repeat_questions (bool): If true, questions may be repeated before all have
                been asked.
            end_early (bool): If true, ends the game when all questions have been asked.
            president_range (tuple[int, int], optional): Range of presidents to include.
            verbose_level (Literal[0, 1, 2], optional): Verbosity level.
        """
        self.repeat_questions = repeat_questions
        self.end_early = end_early
        self.president_range = (
            president_range
            if president_range is not None
            and 1 <= president_range[0] <= president_range[1] <= NUM_PRESIDENTS + 1
            else (1, NUM_PRESIDENTS + 1)
        )
        self.verbose_level = verbose_level if verbose_level in (0, 1, 2) else 1

    def pretty_print(self) -> str:
        """Return a formatted string summarizing all settings for the quiz game.

        Returns:
            str: A string summarizing all configuration fields.
        """
        return (f"repeat_questions={self.repeat_questions}, "
                f"end_early={self.end_early}, "
                f"president_range={self.president_range}, "
                f"verbose_level={self.verbose_level}")

LOGGER = logging.getLogger(__name__)

ALL_PRESIDENTS = [
    President("George", "Washington", ["1"], ["1789"]),
    President("John", "Adams", ["2"], ["1797"]),
    President("Thomas", "Jefferson", ["3"], ["1801"]),
    President("James", "Madison", ["4"], ["1809"]),
    President("James", "Monroe", ["5"], ["1817"]),
    President("John", "Adams", ["6"], ["1825"], middle_name="Quincy"),
    President("Andrew", "Jackson", ["7"], ["1829"]),
    President("Martin", "Van Buren", ["8"], ["1837"]),
    President("William", "Harrison", ["9"], ["1841"], middle_name="Henry"),
    President("John", "Tyler", ["10"], ["1841"]),
    President("James", "Polk", ["11"], ["1845"], middle_name="K."),
    President("Zachary", "Taylor", ["12"], ["1849"]),
    President("Millard", "Fillmore", ["13"], ["1850"]),
    President("Franklin", "Pierce", ["14"], ["1853"]),
    President("James", "Buchanan", ["15"], ["1857"]),
    President("Abraham", "Lincoln", ["16"], ["1861"]),
    President("Andrew", "Johnson", ["17"], ["1865"]),
    President("Ulysses", "Grant", ["18"], ["1869"], middle_name="S."),
    President("Rutherford", "Hayes", ["19"], ["1877"], middle_name="B."),
    President("James", "Garfield", ["20"], ["1881"], middle_name="A."),
    President("Chester", "Arthur", ["21"], ["1881"], middle_name="A."),
    President("Grover", "Cleveland", ["22", "24"], ["1885", "1893"]),
    President("Benjamin", "Harrison", ["23"], ["1889"]),
    President("William", "McKinley", ["25"], ["1897"]),
    President("Theodore", "Roosevelt", ["26"], ["1901"], nickname="Teddy"),
    President("William", "Taft", ["27"], ["1909"], middle_name="Howard"),
    President("Woodrow", "Wilson", ["28"], ["1913"]),
    President("Warren", "Harding", ["29"], ["1921"], middle_name="G."),
    President("Calvin", "Coolidge", ["30"], ["1923"]),
    President("Herbert", "Hoover", ["31"], ["1929"]),
    President("Franklin", "Roosevelt", ["32"], ["1933"], middle_name="D.",
              nickname="FDR"),
    President("Harry", "Truman", ["33"], ["1945"], middle_name="S."),
    President("Dwight", "Eisenhower", ["34"], ["1953"], middle_name="D."),
    President("John", "Kennedy", ["35"], ["1961"], middle_name="F.", nickname="JFK"),
    President("Lyndon", "Johnson", ["36"], ["1963"], middle_name="B."),
    President("Richard", "Nixon", ["37"], ["1969"]),
    President("Gerald", "Ford", ["38"], ["1974"]),
    President("Jimmy", "Carter", ["39"], ["1977"]),
    President("Ronald", "Reagan", ["40"], ["1981"]),
    President("George", "Bush", ["41"], ["1989"], middle_name="H. W."),
    President("Bill", "Clinton", ["42"], ["1993"]),
    President("George", "Bush", ["43"], ["2001"], middle_name="W."),
    President("Barack", "Obama", ["44"], ["2009"]),
    President("Donald", "Trump", ["45", "47"], ["2017", "2025"]),
    President("Joe", "Biden", ["46"], ["2021"]),
]
NUM_PRESIDENTS = len(ALL_PRESIDENTS) # 45 distinct presidents

GAME_STATS = Statistics()
GAME_SETTINGS = Settings()

def format_as_percent(n: int, d: int) -> str:
    """Helper function to format a numerator and denominator as a percent to two decimal places."""
    return f"{(n / d * 100) if d > 0 else 0:.2f}%"

def check_name(given_name: str, president: President) -> bool:
    """Verify the user's input matches the president's name.

    Acceptable formats:
    - first last
    - first middle last
    - middle last
    - nickname
    - last
    If the given input is ambiguous (e.g., "John Adams"), return False.
    """
    first_last = president.first_name.lower() + " " + president.last_name.lower()

    if president.middle_name is not None:
        first_middle_last = president.first_name.lower() + " " + president.middle_name.lower() + " " + president.last_name.lower()
        middle_last = president.middle_name.lower() + " " + president.last_name.lower()
        # ignore periods in middle initial
        first_middle_last = first_middle_last.replace(".", "")
        middle_last = middle_last.replace(".", "")
    else:
        first_middle_last = None
        middle_last = None

    nickname = None if president.nickname is None else president.nickname.lower()

    last = president.last_name.lower()
    # strip whitespace and remove dots
    given_name = given_name.lower().strip().replace(".", "")

    # if half-ambiguous, go with no-middle-name option
    # right now, this is only john adams
    # e.g., "John Adams" -> John Adams (1797)
    # "John Quincy Adams" -> John Quincy Adams (1825)
    if given_name == first_last and first_last in president.HALF_AMBIGIOUS_FULL_NAMES \
        and president.middle_name is None:
        return True

    # explicity check for ambiguous names
    if first_last == given_name and given_name not in president.AMBIGIOUS_FULL_NAMES:
        return True

    if first_middle_last == given_name:
        return True

    # e.g., "Quincy Adams" -> John Quincy Adams (1825)
    if middle_last == given_name:
        return True

    # e.g., "Teddy" -> Theodore Roosevelt (1901)
    if nickname == given_name:
        return True

    # explicity check for ambiguous last names
    if last == given_name and given_name not in president.AMBIGIOUS_LAST_NAMES:
        return True

    # warn on ambiguous name
    if given_name in president.AMBIGIOUS_FULL_NAMES + president.AMBIGIOUS_LAST_NAMES:
        LOGGER.warning("Ambiguous name provided: '%s'", given_name)

    return False

def check_order(given_order: str, president: President) -> bool:
    """Verify the user's input matches the president's order number(s)."""
    given_order = given_order.strip()

    if len(president.order_numbers) > 1:
        return given_order == " ".join(president.order_numbers)

    return given_order == president.order_numbers[0]

def check_year(given_year: str, president: President) -> bool:
    """Verify the user's input matches the president's start year(s)."""
    given_year = given_year.strip()

    if len(president.start_year) > 1:
        return given_year == " ".join(president.start_year)

    return given_year == president.start_year[0]

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

    # TODO: add "nice" option (accepts ambigious names)
    # TODO: add levenshtein distance option for typos
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

    # TODO: move to logging setup function
    # Update logging level based on verbosity
    if settings.verbose_level == settings.VERBOSE_QUIET:
        LOGGER.setLevel(logging.ERROR)
    elif settings.verbose_level == settings.VERBOSE_VERBOSE:
        LOGGER.setLevel(logging.DEBUG)
    else: # settings.VERBOSE_NORMAL
        LOGGER.setLevel(logging.INFO)

    # Add a formatter that changes format based on severity
    class SeverityFormatter(logging.Formatter):
        FORMATS: ClassVar[dict[int, str]] = {
            logging.DEBUG: "[DEBUG] %(message)s",
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
    LOGGER.addHandler(handler)

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
        question_type = random.choice(["year", "order", "name"])
        # TODO: more elegant solution for ambiguous years
        if current_president.is_year_ambiguous():
            question_type = random.choice(["name", "order"])

        if question_type == "year":
            start_year_str = " and ".join(current_president.start_year)

            print(f"Year = {start_year_str}:")
            user_name = input("Who was the president? ")
            check_name_result = check_name(user_name, current_president)
            user_order = input("What was the order number? (if multiple, separate with spaces) ")
            check_order_result = check_order(user_order, current_president)

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
            check_name_result = check_name(user_name, current_president)
            user_year = input("What year did they start their term? (if multiple, separate with spaces) ")
            check_year_result = check_year(user_year, current_president)

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
            check_order_result = check_order(user_order, current_president)
            user_year = input("What year did they start their term? (if multiple, separate with spaces) ")
            check_year_result = check_year(user_year, current_president)

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
