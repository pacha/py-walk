from typing import Optional
from pathlib import Path

from gitignore_match.models import PatternCollection

def parse_pattern_list(pattern_list: list[str], base_dir: Path) -> PatternCollection:
    """Create a PatternCollection object from a list of patterns."""
    return PatternCollection(pattern_list, base_dir)
