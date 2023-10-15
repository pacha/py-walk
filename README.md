<p align="center">
    <img src="https://raw.githubusercontent.com/pacha/gitignore-match/main/docs/logo-header.png" alt="logo">
</p>

gitignore-match
===============

![Tests](https://github.com/pacha/gitignore-match/actions/workflows/tests.yaml/badge.svg)
![Type checks](https://github.com/pacha/gitignore-match/actions/workflows/type-checks.yaml/badge.svg)
![Code formatting](https://github.com/pacha/gitignore-match/actions/workflows/code-formatting.yaml/badge.svg)
![Supported Python versions](https://img.shields.io/pypi/pyversions/gitignore-match.svg)

_Python library to match files against gitignore-type patterns which aims to be nearly* 100% compatible with Git's implementation._

\* Currently, POSIX extended character classes like `[: :]`, `[. .]` or `[= =]` aren't supported.

> To guarantee the utmost compatibility with Git's behavior, `gitignore-match` is
> run through hundreds of tests. These tests are designed to compare the
> library's results with those of Git itself, ensuring they align as closely as
> possible.

## Usage

Passing patterns using a file:
```python
from gitignore_match import get_parser_from_file

parser = get_parser_from_file("path/to/gitignore-type-file")
if parser.match("file.txt"):
    ...
```

Passing patterns using a string:
```python
from gitignore_match import get_parser_from_text

patterns = """
# some comment
*.txt
**/bar/*.dat
"""

parser = get_parser_from_text(patterns, base_dir="/some/folder")
if parser.match("file.txt"):
    ...
```

Passing patterns using a list:
```python
from gitignore_match import get_parser_from_text

patterns = [
    "*.txt",
    "**/bar/*.dat",
]

parser = get_parser_from_list(patterns, base_dir="/some/folder")
if parser.match("file.txt"):
    ...
```

## Installation

To install cells, simply use `pip`:
```shell
$ pip install gitignore-match
```

