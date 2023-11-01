import os
from typing import List
from typing import Union
from pathlib import Path
from dataclasses import dataclass

from gitignore_match.exceptions import GitignoreMatchInputError
from gitignore_match.logs import log
from .pattern import Pattern


@dataclass
class Parser:
    patterns: List[Pattern]
    base_dir: Path

    def __init__(self, glob_pattern_list: List[str], base_dir: Path):
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
        path_is_dir = full_path.is_dir() or trailing_slash

        # match against each pattern
        matched_patterns: list[int] = []
        log.debug(f"\n-- Matching path: {relative_path} (is_dir: {path_is_dir})")

        for pattern in self.patterns:
            log.debug(f"- {pattern} (history: {matched_patterns})")
            # if no match found, skip negative patterns
            if pattern.negated and not matched_patterns:
                continue

            # check if pattern matches
            matched_parts = pattern.match(relative_path, path_is_dir)
            log.debug(f"- Matched parts {matched_parts})")
            if matched_parts:
                if pattern.negated:
                    if set(matched_patterns) - set(matched_parts):
                        log.debug("- Not negated!")
                    else:
                        log.debug("- Negated!")
                        matched_patterns = []
                else:
                    log.debug("- Matched!")
                    matched_patterns.extend(matched_parts)
        return bool(matched_patterns)
