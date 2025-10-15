import pathlib
import sys

# allow python . to work
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "src"))

from presidents_quiz.main import cli as _cli

if __name__ == "__main__":
    _cli()
