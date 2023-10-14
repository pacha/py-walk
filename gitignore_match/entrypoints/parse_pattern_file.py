from typing import Union
from pathlib import Path

from gitignore_match.models import PatternCollection
from .parse_pattern_list import parse_pattern_list

def parse_pattern_file(path: Union[Path, str]) -> PatternCollection:
    """Create a PatternCollection object from a gitignore-type file."""

    comment_leader = "#"

    # normalize input to Path
    if isinstance(path, str):
        path = Path(path)

    # extract patterns
    patterns = []
    with path.open() as f:
        for line in f.readlines():
            # discard non-pattern lines
            l_clean_line = line.lstrip()
            if not l_clean_line or l_clean_line.startswith(comment_leader):
                continue

            r_clean_line = line.rstrip()
            patterns.append(r_clean_line)

    base_dir = path.parent
    return parse_pattern_list(patterns, base_dir=base_dir)
