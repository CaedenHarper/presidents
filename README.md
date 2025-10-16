# Presidents

This project includes `src/presidents_quiz/main.py`, a Python CLI for memorizing the order of US Presidents.

## Features

- Game to memorize the order of US Presidents, the names of US Presidents, and the years they were inaugurated
- Customizable guessing range and game settings

## Usage

- You can run the CLI using `python .`, `python -m presidents_quiz`, or `python src/presidents_quiz/main.py`

```bash
python . [-h] [-r | -e] [-a] [-R START END] [-v {0,1,2}]

Quiz game for US presidents.

options:
  -h, --help            show this help message and exit
  -r, --repeat          Allows repeat questions before all questions have been exhausted. Can not be used with --end-early. (Default: false)     
  -e, --end-early       Ends questions when all have been asked. Can not be used with --repeat. (Default: false)
  -a, --allow-ambiguity
                        Allows amibguous answers. For example, 'John Adams' will count for both presidents if this flag is true. (Default: false)
  -R, --range START END
                        Range of presidents to include, (1-45). (Default: all)
  -v, --verbosity {0,1,2}
                        Verbosity level: 0 = quiet, 1 = normal, 2 = verbose. (Default: 1)
```

## Requirements

- Tested with Python >= 3.10
- No additional dependencies required to run the CLI
- See `requirements.txt` for testing requirements

## Testing

- Testing is done automatically on PR to main
- Testing consists of Ruff linting, Pyright type checking, and Pytest tests
- You can run the tests locally as well:
```bash
# create and populate a venv however you'd like
uv venv
.venv\Scripts\activate
uv pip install -r requirements.txt
# if developing locally, ensure pacakge is in venv
# if you don't you will get import errors in tests/
uv pip install -e .
# linting
python -m ruff check .
# type checking
python -m pyright .
# pytests
python -m pytest .
```