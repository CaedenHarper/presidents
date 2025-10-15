__all__ = ["QuizStatistics"]

class QuizStatistics:
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
        return (f"total_questions={self.total_questions}, "
                f"correct_questions={self.correct_questions}, "
                f"half_correct_questions={self.half_correct_questions}, "
                f"correct_names={self.correct_names}, "
                f"name_questions={self.name_questions}, "
                f"correct_orders={self.correct_orders}, "
                f"order_questions={self.order_questions}, "
                f"correct_years={self.correct_years}, "
                f"year_questions={self.year_questions}")
