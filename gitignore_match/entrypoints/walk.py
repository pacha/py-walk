from typing import Union
from typing import Callable
from typing import Generator
from pathlib import Path

from gitignore_match.exceptions import GitignoreMatchInputError
from .get_parser_from_list import get_parser_from_list
from .get_parser_from_text import get_parser_from_text


def walk(
    base_dir: Union[Path, str],
    include: Union[str, list[str], None] = None,
    exclude: Union[str, list[str], None] = None,
) -> Generator[Path, None, None]:
    """Return all the children under a given path that match the provided filters."""

    # normalize path to Path
    if isinstance(base_dir, str):
        base_dir = Path(base_dir)
    if not base_dir.is_dir():
        raise GitignoreMatchInputError(f"Not a directory: '{base_dir}'")

    # get include parser
    if isinstance(include, str):
        include_parser = get_parser_from_text(include, base_dir).match
    elif isinstance(include, list):
        include_parser = get_parser_from_list(include, base_dir).match
    elif include is None:
        include_parser = lambda path: True
    else:
        raise GitignoreMatchInputError(
            "'include' must be a string or a list of patterns"
        )

    # get include parser
    if isinstance(exclude, str):
        exclude_parser = get_parser_from_text(exclude, base_dir).match
    elif isinstance(exclude, list):
        exclude_parser = get_parser_from_list(exclude, base_dir).match
    elif exclude is None:
        exclude_parser = lambda path: False
    else:
        raise GitignoreMatchInputError(
            "'exclude' must be a string or a list of patterns"
        )

    # walk children
    for child in base_dir.iterdir():
        yield from walk_rec(child, include_parser, exclude_parser)


def walk_rec(
    path: Path,
    include_parser: Callable[[Path], bool],
    exclude_parser: Callable[[Path], bool],
) -> Generator[Path, None, None]:
    if include_parser(path) and not exclude_parser(path):
        yield path
        if path.is_dir():
            for child in path.iterdir():
                yield from walk_rec(child, include_parser, exclude_parser)
