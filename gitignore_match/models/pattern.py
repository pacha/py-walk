import re
from sly.lex import LexError
from dataclasses import field
from dataclasses import dataclass

from gitignore_match.lib.gitglob_to_regex import gitglob_to_regex

path_name_pattern = re.compile(r"[^/]+/?$")


@dataclass
class Pattern:
    glob: str
    regex: re.Pattern = field(init=False)
    negated: bool = False

    def __post_init__(self):
        # parse negation prefix (!)
        inner_glob = self.glob
        if self.glob.startswith("!"):
            self.negated = True
            inner_glob = self.glob[1:]

        # get regex
        try:
            self.regex = gitglob_to_regex(inner_glob)
        except LexError:
            self.regex = re.compile("(?!)")

    def match(self, path: str) -> bool:
        return bool(self.regex.search(path))

    def __str__(self):
        return f"Glob: {self.glob} Regex: {self.regex.pattern}{ ' (negated)' if self.negated else ''}"
