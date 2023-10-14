import os
from typing import Union
from typing import Optional
from pathlib import Path
from dataclasses import dataclass

from gitignore_match.exceptions import GitignoreMatchInputError
from .pattern import Pattern

@dataclass
class PatternCollection:
    patterns: list[Pattern]
    base_dir: Path

    def __init__(self, glob_pattern_list: list[str], base_dir: Path):
        self.patterns = []
        for glob_pattern in glob_pattern_list:
            self.patterns.append(Pattern(glob_pattern))
        self.base_dir = base_dir

    def match(self, path: Union[Path, str]) -> Optional[Pattern]:
        # normalize input to string with trailing slash for directories
        if isinstance(path, str):
            path = Path(path)
        # if not path.is_relative_to(self.base_dir):
        #     raise GitignoreMatchInputError(
        #         f"Error: path '{path}' is not relative to base dir '{self.base_dir}'"
        #     )
        full_path = self.base_dir / path
        suffix = os.sep if full_path.is_dir() else ""
        path = f"{path}{suffix}"

        # match against each pattern
        for pattern in self.patterns:
            if pattern.match(path):
                return pattern

        # return nothing if no match
        return None
