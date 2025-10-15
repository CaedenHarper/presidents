from presidents_quiz.quiz_statistics import QuizStatistics


def test_initial_state_is_zero() -> None:
    s = QuizStatistics()
    assert s.total_questions == 0
    assert s.correct_questions == 0
    assert s.half_correct_questions == 0
    assert s.correct_names == 0
    assert s.name_questions == 0
    assert s.correct_orders == 0
    assert s.order_questions == 0
    assert s.correct_years == 0
    assert s.year_questions == 0


# record_year_question

def test_record_year_question_both_correct() -> None:
    s = QuizStatistics()
    s.record_year_question(correct_name=True, correct_order=True)

    assert s.total_questions == 1
    assert s.name_questions == 1
    assert s.order_questions == 1

    # both correct -> counts increment
    assert s.correct_questions == 1
    assert s.half_correct_questions == 1
    assert s.correct_names == 1
    assert s.correct_orders == 1

    # no year fields touched here
    assert s.year_questions == 0
    assert s.correct_years == 0


def test_record_year_question_half_correct_name_only() -> None:
    s = QuizStatistics()
    s.record_year_question(correct_name=True, correct_order=False)

    assert s.total_questions == 1
    assert s.name_questions == 1
    assert s.order_questions == 1

    # half correct
    assert s.correct_questions == 0
    assert s.half_correct_questions == 1
    assert s.correct_names == 1
    assert s.correct_orders == 0


def test_record_year_question_none_correct() -> None:
    s = QuizStatistics()
    s.record_year_question(correct_name=False, correct_order=False)

    assert s.total_questions == 1
    assert s.name_questions == 1
    assert s.order_questions == 1

    # none correct -> no correct or half-correct increments
    assert s.correct_questions == 0
    assert s.half_correct_questions == 0
    assert s.correct_names == 0
    assert s.correct_orders == 0


# record_order_question

def test_record_order_question_both_correct() -> None:
    s = QuizStatistics()
    s.record_order_question(correct_name=True, correct_year=True)

    assert s.total_questions == 1
    assert s.name_questions == 1
    assert s.year_questions == 1

    assert s.correct_questions == 1
    assert s.half_correct_questions == 1
    assert s.correct_names == 1
    assert s.correct_years == 1

    # no order fields touched here
    assert s.order_questions == 0
    assert s.correct_orders == 0


def test_record_order_question_half_correct_year_only() -> None:
    s = QuizStatistics()
    s.record_order_question(correct_name=False, correct_year=True)

    assert s.total_questions == 1
    assert s.name_questions == 1
    assert s.year_questions == 1

    assert s.correct_questions == 0
    assert s.half_correct_questions == 1
    assert s.correct_names == 0
    assert s.correct_years == 1


def test_record_order_question_none_correct() -> None:
    s = QuizStatistics()
    s.record_order_question(correct_name=False, correct_year=False)

    assert s.total_questions == 1
    assert s.name_questions == 1
    assert s.year_questions == 1

    assert s.correct_questions == 0
    assert s.half_correct_questions == 0
    assert s.correct_names == 0
    assert s.correct_years == 0


# record_name_question

def test_record_name_question_both_correct() -> None:
    s = QuizStatistics()
    s.record_name_question(correct_order=True, correct_year=True)

    assert s.total_questions == 1
    assert s.order_questions == 1
    assert s.year_questions == 1

    assert s.correct_questions == 1
    assert s.half_correct_questions == 1
    assert s.correct_orders == 1
    assert s.correct_years == 1

    # no name fields touched here
    assert s.name_questions == 0
    assert s.correct_names == 0


def test_record_name_question_half_correct_order_only() -> None:
    s = QuizStatistics()
    s.record_name_question(correct_order=True, correct_year=False)

    assert s.total_questions == 1
    assert s.order_questions == 1
    assert s.year_questions == 1

    assert s.correct_questions == 0
    assert s.half_correct_questions == 1
    assert s.correct_orders == 1
    assert s.correct_years == 0


def test_record_name_question_none_correct() -> None:
    s = QuizStatistics()
    s.record_name_question(correct_order=False, correct_year=False)

    assert s.total_questions == 1
    assert s.order_questions == 1
    assert s.year_questions == 1

    assert s.correct_questions == 0
    assert s.half_correct_questions == 0
    assert s.correct_orders == 0
    assert s.correct_years == 0


# cumulative behavior

def test_cumulative_increments_across_mixed_calls() -> None:
    s = QuizStatistics()
    # year: both correct
    s.record_year_question(correct_name=True, correct_order=True)
    # order: half correct (year only)
    s.record_order_question(correct_name=False, correct_year=True)
    # name: none correct
    s.record_name_question(correct_order=False, correct_year=False)

    assert s.total_questions == 3
    assert s.correct_questions == 1
    assert s.half_correct_questions == 2

    # name stats: one correct (from first call), two name questions overall (year+order paths)
    assert s.name_questions == 2
    assert s.correct_names == 1

    # order stats: two order questions overall (year+name paths), one correct (first call)
    assert s.order_questions == 2
    assert s.correct_orders == 1

    # year stats: two year questions overall (order+name paths), one correct (second call)
    assert s.year_questions == 2
    assert s.correct_years == 1

def test_pretty_print() -> None:
    s = QuizStatistics()
    # year: both correct
    s.record_year_question(correct_name=True, correct_order=True)
    # order: half correct (year only)
    s.record_order_question(correct_name=False, correct_year=True)
    # name: none correct
    s.record_name_question(correct_order=False, correct_year=False)

    expected = ("total_questions=3, correct_questions=1, half_correct_questions=2, correct_names=1, name_questions=2, "
                "correct_orders=1, order_questions=2, correct_years=1, year_questions=2")
    assert s.pretty_print() == expected
