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
        suffix = os.sep if full_path.is_dir() or trailing_slash else ""
        path_str = f"{relative_path.as_posix()}{suffix}"

        # match against each pattern
        match_found = False
        matched_patterns = {
            "positive": [],
            "negative": [],
        }
        log.debug("\n-- Matching")
        log.debug(f"Path: '{path_str}'")

        for pattern in self.patterns:

            # if no match found, skip negative patterns
            if not match_found and pattern.negated:
                continue

            # check if pattern matches
            if pattern.match(path_str):
                if pattern.negated:
                    matched_patterns["negative"].append(pattern)
                    if not is_parent_dir_excluded(relative_path, matched_patterns["positive"]):
                        match_found = False
                        log.debug(f"- {pattern} [Match!]")
                    else:
                        log.debug(f"- Glob: {pattern.glob} [skipped: parent directory already matched]")
                else:
                    matched_patterns["positive"].append(pattern)
                    match_found = True
                    log.debug(f"- {pattern} [Match!]")
        return match_found


def is_parent_dir_excluded(relative_path: Path, already_matched_patterns: list[Pattern]):
    # get path components
    parent_paths_str = list(reversed([
        f"{parent.as_posix()}{os.sep}" for parent in relative_path.parents
    ]))
    if len(parent_paths_str) < 2:
        return False

    # divide path directories into three categories
    # ('root' is always Path('.') for relative paths)
    root, *ancestors, parent = parent_paths_str
    for ancestor in ancestors:
        for matched_pattern in already_matched_patterns:
            if matched_pattern.match(ancestor):
                return True
    for matched_pattern in already_matched_patterns:
        if not matched_pattern.glob.endswith('*') and matched_pattern.match(parent):
            return True
    return False
