from presidents import NUM_PRESIDENTS

__all__ = ["QuizSettings"]

class QuizSettings:
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
