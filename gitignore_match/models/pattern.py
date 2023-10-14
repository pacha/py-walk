import re
from sly.lex import LexError
from dataclasses import field
from dataclasses import dataclass

from gitignore_match.logs import log
from gitignore_match.lib.git_glob_parser import convert_to_regex

path_name_pattern = re.compile(r"[^/]+/?$")

@dataclass
class Pattern:
    glob: str
    regex: str = field(init=False)
    anchored: bool = field(init=False)
    negated: bool = field(init=False)

    def __post_init__(self):
        try:
            self.regex, self.anchored, self.negated = convert_to_regex(self.glob)
        except LexError:
            self.regex = re.compile("(?!)")
            self.anchored = True
            self.negated = False

    def match(self, path: str) -> bool:
        # if not anchored, only take the name of the path
        if not self.anchored:
            path = path_name_pattern.search(path).group(0)
        log.debug(f"actual path: {path}")

        # XOR
        return bool(self.regex.search(path)) != bool(self.negated)
