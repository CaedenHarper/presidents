# Presidents

This project includes `presidents.py`, a Python script for memorizing the order of US Presidents.

## Features

- Game to memorize the order of US Presidents, the names of US Presidents, and the years they were inaugurated
- Customizable guessing range and game settings

## Usage

```bash
python presidents.py [-h | --help] [-r | --repeat] [-R | --range START END] [-v | --verbose {0,1,2}]

options:
  -h, --help            show this help message and exit
  -r, --repeat          Allows repeat questions before all questions have been exhausted. Can not be used with --end-early. (Default: false)
  -e, --end-early       Ends questions when all have been asked. Can not be used with --repeat. (Default: false)
  -R, --range START END
                        Range of presidents to include (1-45). (Default: all)
  -v, --verbose {0,1,2}
                        Verbosity level: 0 = quiet, 1 = normal, 2 = verbose. (Default: 1)
```

## Requirements

- Tested with Python 3.14, should work with Python versions >= 3.10