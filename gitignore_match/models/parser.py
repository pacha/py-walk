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
            if pattern.match(path_str) is not None:
                if pattern.negated:
                    matched_patterns["negative"].append(pattern)
                    if not is_parent_dir_excluded(
                        path_str, pattern, matched_patterns["positive"]
                    ):
                        match_found = False
                        log.debug(f"- {pattern} [Match!]")
                    else:
                        log.debug(
                            f"- Glob: {pattern.glob} [skipped: parent directory already matched]"
                        )
                else:
                    matched_patterns["positive"].append(pattern)
                    match_found = True
                    log.debug(f"- {pattern} [Match!]")
        return match_found


def is_parent_dir_excluded(
    path_str: str, negated_pattern: Pattern, already_matched_patterns: list[Pattern]
):
    match = negated_pattern.match(path_str)
    for pattern in already_matched_patterns:
        log.debug(f"-- parent check: {match} vs {pattern.regex.pattern}")
        if not pattern.fullmatch(match):
            log.debug(f"-- parent excluded: {pattern.regex.pattern}")
            return True
    log.debug("-- no parent excluded")
    return False

def is_parent_dir_excluded5(
    relative_path: Path, negated_pattern: Pattern, already_matched_patterns: list[Pattern]
):
    path_str = str(relative_path)
    negated_pattern_match = negated_pattern.inner_regex.search(path_str).group(0)
    try:
        next_char = path_str[len(negated_pattern_match)]
    except IndexError:
        next_char = ""
    log.debug(f"-- next char: {next_char}")
    if next_char == os.sep:
        negated_pattern_match += os.sep
    for pattern in already_matched_patterns:
        log.debug(f"-- parent check: {negated_pattern_match} vs {pattern.inner_regex.pattern}")
        if not pattern.inner_fullmatch(negated_pattern_match):
            log.debug(f"-- parent excluded: {pattern.inner_regex.pattern}")
            return True
    log.debug("-- no parent excluded")
    return False

def is_parent_dir_excluded4(
    relative_path: Path, already_matched_patterns: list[Pattern]
):
    for pattern in already_matched_patterns:
        log.debug(f"-- parent check: {str(relative_path)} vs {pattern.inner_regex.pattern}")
        if not pattern.inner_match(str(relative_path)):
            log.debug(f"-- parent excluded: {pattern.inner_regex.pattern}")
            return True
    log.debug("-- no parent excluded")
    return False

def is_parent_dir_excluded3(
    relative_path: Path, already_matched_patterns: list[Pattern]
):
    parents = list(
        reversed([f"{parent.as_posix()}{os.sep}" for parent in relative_path.parents])
    )[1:]
    log.debug(f"-- Testing parents: {parents}")
    flagged = False
    for parent in parents:
        log.debug(f"-- parent: {parent}")
        for pattern in already_matched_patterns:
            log.debug(f"-- pattern: {pattern.inner_regex.pattern}")
            if pattern.match(parent):
                if not flagged:
                    log.debug("-- flagged!")
                    flagged = True
                else:
                    log.debug("-- matched!")
                    return True
    return False

def is_parent_dir_excluded2(
    relative_path: Path, already_matched_patterns: list[Pattern]
):
    # get path components
    parent_paths_str = list(
        reversed([f"{parent.as_posix()}{os.sep}" for parent in relative_path.parents])
    )
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
        if (
            not matched_pattern.glob.endswith("*") or matched_pattern.glob == "*"
        ) and matched_pattern.match(parent):
            return True
    return False
