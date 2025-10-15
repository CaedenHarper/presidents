# allow python src/presidents_quiz or python -m src/presidents_quiz to work
from presidents_quiz.main import cli as _cli

if __name__ == "__main__":
    _cli()
