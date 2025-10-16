import logging

from presidents_quiz.presidents import NUM_PRESIDENTS

__all__ = ["QuizSettings"]

LOGGER = logging.getLogger(__name__)

class QuizSettings:
    """Stores configuration settings for the quiz game.

    Attributes:
        VERBOSE_QUIET (Literal[0]): Verbose quiet magic number.
        VERBOSE_NORMAL (Literal[1]): Verbose normal magic number.
        VERBOSE_VERBOSE (Literal[2]): Verbose verbose magic number.
        POSSIBLE_VERBOSE_LEVELS (tuple[int]): Possible verbosity numbers.

        repeat_questions (bool): If true, questions may be repeated before all have been asked.
        end_early (bool): If true, ends the game when all questions have been asked.
        president_range (tuple[int, int]): Range of presidents to include.
        verbose_level (Literal[0, 1, 2]): Verbosity level.
        allow_ambiguity (bool): If true, ambiguous answers are allowed.
    """

    VERBOSE_QUIET = 0
    VERBOSE_NORMAL = 1
    VERBOSE_VERBOSE = 2
    POSSIBLE_VERBOSE_LEVELS = (VERBOSE_QUIET, VERBOSE_NORMAL, VERBOSE_VERBOSE)

    def __init__(self) -> None:
        """Initialize Settings with default configuration options."""
        self.repeat_questions = False
        self.end_early = False
        self.president_range = (1, NUM_PRESIDENTS + 1)
        self.verbose_level = 1
        self.allow_ambiguity = False

    def update(self,
               *,
               repeat_questions: bool | None = None,
               end_early: bool | None = None,
               allow_ambiguity: bool | None = None,
               president_range: tuple[int, int] | None = None,
               verbose_level: int | None = None) -> None:
        """Update settings flags."""
        if self.repeat_questions is not None:
            self.repeat_questions = repeat_questions
        if self.end_early is not None:
            self.end_early = end_early
        if allow_ambiguity is not None:
            self.allow_ambiguity = allow_ambiguity
        if president_range is not None:
            # fallback to default range if outside of range
            if 1 <= president_range[0] <= president_range[1] <= NUM_PRESIDENTS + 1:
                self.president_range = president_range
            else:
                LOGGER.warning("Range arguments not possible. Setting back to default of (1, %s).", NUM_PRESIDENTS + 1)
        if verbose_level is not None:
            # fallback to default verbosity if outside of range
            if verbose_level in self.POSSIBLE_VERBOSE_LEVELS:
                self.verbose_level = verbose_level
            else:
                LOGGER.warning("Verbose argument not possible. Setting back to default of 1.")

    def pretty_print(self) -> str:
        """Return a formatted string summarizing all settings for the quiz game.

        Returns:
            str: A string summarizing all configuration fields.
        """
        return (f"repeat_questions={self.repeat_questions}, "
                f"end_early={self.end_early}, "
                f"allow_ambiguity={self.allow_ambiguity}, "
                f"president_range={self.president_range}, "
                f"verbose_level={self.verbose_level}")
