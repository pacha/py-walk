from typing import Union
from pathlib import Path

from gitignore_match.models import Parser
from .get_parser_from_list import get_parser_from_list

COMMENT_LEADER = "#"


def get_parser_from_text(text: str, base_dir: Union[Path, str]) -> Parser:
    """Create a Parser object from a multiline text."""

    # normalize base_dir to Path
    if isinstance(base_dir, str):
        base_dir = Path(base_dir)

    glob_patterns = []
    for line in text.splitlines():
        # discard non-pattern lines
        clean_line = line.lstrip()
        if not clean_line or clean_line.startswith(COMMENT_LEADER):
            continue

        glob_patterns.append(clean_line)

    return get_parser_from_list(glob_patterns, base_dir=base_dir)
