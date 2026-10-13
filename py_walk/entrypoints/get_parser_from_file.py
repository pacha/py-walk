from typing import Union
from pathlib import Path

from py_walk.models import Parser
from .get_parser_from_text import get_parser_from_text


def get_parser_from_file(path: Union[Path, str]) -> Parser:
    """Create a Parser object from a gitignore-type file."""

    # normalize path to Path
    if isinstance(path, str):
        path = Path(path)

    # read the file as UTF-8 whatever the locale, so that the patterns do not
    # depend on the machine
    text = path.read_text(encoding="utf-8")
    base_dir = path.parent
    return get_parser_from_text(text, base_dir=base_dir)
