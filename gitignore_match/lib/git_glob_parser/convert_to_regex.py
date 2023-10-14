
import re
import fnmatch
from .glob_lexer import glob_lexer

from gitignore_match.logs import log

anchoring_tokens = {"SLASH", "DOUBLE_STAR_MIDDLE"}

regex_map = {
    "ESC_SQUARE_BRACKET": r"\[",
    "ESC_EXCLAMATION_MARK": r"!",
    "ESC_QUESTION_MARK": r"\?",
    "ESC_STAR": r"\*",
    "DOUBLE_STAR_START": r".*/",
    "DOUBLE_STAR_END": r".*$",
    "DOUBLE_STAR_MIDDLE": r"/.*/",
    "SLASH_END": r"/$",
    "SLASH": r"/",
    "QUESTION_MARK": r"[^/]",
    "STAR": r"[^/]*",
}

def convert_to_regex(glob_pattern: str) -> re.Pattern:
    tokens = list(glob_lexer.tokenize(glob_pattern))
    token_types = [token.type for token in tokens]
    if not token_types:
        return re.compile("^$")
    anchored = bool(anchoring_tokens & set(token_types))

    # if not anchored, DOUBLE_STAR_START is superfluous
    if not anchored and token_types[0] == "DOUBLE_STAR_START":
        del tokens[0]

    # exclamation mark negates the entire expression
    negated = token_types[0] == "EXCLAMATION_MARK"
    if negated:
        del tokens[0]

    regex = "^"
    log.debug(f"glob: {glob_pattern}")
    for token in tokens:
        log.debug(f"- token: {token.type} ({token.value})")
        if token.type == "CHARACTER_CLASS":
            regex += fnmatch.translate(token.value)[4:-3]
        else:
            regex += regex_map.get(token.type, token.value)
    regex += "$"
    log.debug(f"regex: {'not(' * negated}{regex}{')' * negated}")
    return re.compile(regex), anchored, negated
