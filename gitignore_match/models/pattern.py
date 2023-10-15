import re
from sly.lex import LexError
from dataclasses import field
from dataclasses import dataclass

from gitignore_match.logs import log
from gitignore_match.lib.gitglob_to_regex import gitglob_to_regex

path_name_pattern = re.compile(r"[^/]+/?$")

@dataclass
class Pattern:
    glob: str
    regex: str = field(init=False)

    def __post_init__(self):
        try:
            self.regex = gitglob_to_regex(self.glob)
        except LexError:
            self.regex = re.compile("(?!)")

    def match(self, path: str) -> bool:
        # if not anchored, only take the name of the path
        # if not self.anchored:
        #     path = path_name_pattern.search(path).group(0)
        # log.debug(f"actual path: {path}")

        # # XOR
        # return bool(self.regex.search(path)) != bool(self.negated)
        # path = path if path.startswith("/") else f"/{path}"
        log.debug(f"actual path: {path}")
        log.debug(f"regex: {self.regex.pattern}")
        return bool(self.regex.search(path))
