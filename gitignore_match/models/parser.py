import os
from typing import Union
from pathlib import Path
from dataclasses import dataclass

from gitignore_match.exceptions import GitignoreMatchInputError
from gitignore_match.logs import log
from .pattern import Pattern


@dataclass
class Parser:
    patterns: list[Pattern]
    base_dir: Path

    def __init__(self, glob_pattern_list: list[str], base_dir: Path):
        self.patterns = []
        for glob_pattern in glob_pattern_list:
            log.debug("\n-- Regex building")
            pattern = Pattern(glob_pattern)
            log.debug(f"{pattern}")
            self.patterns.append(pattern)
        self.base_dir = base_dir

    def match(self, path: Union[Path, str]) -> bool:
        # normalize pathlib.Path
        trailing_slash = path.endswith(os.sep) if isinstance(path, str) else False
        full_path = self.base_dir / Path(path)

        # directory paths always have a trailing slash so the Pattern
        # class doesn't have to access disk
        try:
            relative_path = full_path.relative_to(self.base_dir)
        except ValueError:
            raise GitignoreMatchInputError(
                f"Error: path '{path}' is not relative to base dir '{self.base_dir}'"
            )
        suffix = os.sep if full_path.is_dir() or trailing_slash else ""
        path_str = f"{relative_path.as_posix()}{suffix}"

        # match against each pattern
        match_found = False
        log.debug("\n-- Matching")
        log.debug(f"Path: '{path_str}'")
        for pattern in self.patterns:
            if pattern.match(path_str):
                match_found = not pattern.negated
                log.debug(f"{pattern} [Match!]")
            else:
                log.debug(f"{pattern}")
        return match_found
