# mypy: disable-error-code="name-defined"
import re
import fnmatch
from typing import Tuple

from sly import Lexer

from gitignore_match.logs import log
from .character_class_to_regex import character_class_to_regex


class GlobLexer(Lexer):
    tokens = {  # noqa
        ESC_EXCLAMATION_MARK,  # noqa
        ESC_SQUARE_BRACKET,  # noqa
        ESC_QUESTION_MARK,  # noqa
        ESC_SPACE,  # noqa
        ESC_STAR,  # noqa
        DOUBLE_STAR_START,  # noqa
        DOUBLE_STAR_END,  # noqa
        CHARACTER_CLASS,  # noqa
        TRAILING_SPACE,  # noqa
        QUESTION_MARK,  # noqa
        DOUBLE_STAR,  # noqa
        SPACE,  # noqa
        STAR_END,  # noqa
        STAR,  # noqa
        SLASH_START,  # noqa
        SLASH_END,  # noqa
        SLASH,  # noqa
        TEXT,  # noqa
    }

    ESC_EXCLAMATION_MARK = r"\\!"
    ESC_SQUARE_BRACKET = r"\\\["
    ESC_QUESTION_MARK = r"\\\?"
    ESC_SPACE = r"\\ "
    ESC_STAR = r"\\\*"
    DOUBLE_STAR_END = r"/?\*\*/$"
    DOUBLE_STAR_START = r"^((\*\*/)|(/\*\*/))"
    CHARACTER_CLASS = r"\[(\^|!)?\]?-?(\[:[a-z]+:\]|(\\\]|\\-|[^]-])-(\\\]|\\-|[^]-])|\\\]|\\-|[^]-])*-?\]"
    TRAILING_SPACE = r"\s+$"
    QUESTION_MARK = r"\?"
    DOUBLE_STAR = r"/\*\*/"
    SPACE = r" "
    STAR_END = r"\*$"
    STAR = r"\*"
    SLASH_START = r"^/"
    SLASH_END = r"/$"
    SLASH = r"/"
    TEXT = r"[^/[ \\?]+"


glob_lexer = GlobLexer()

regex_map = {
    "ESC_EXCLAMATION_MARK": r"!",
    "ESC_QUESTION_MARK": r"\?",
    "ESC_SQUARE_BRACKET": r"\[",
    "ESC_SPACE": r"\ ",
    "ESC_STAR": r"\*",
    "TRAILING_SPACE": r"",
    "QUESTION_MARK": r".",
    "DOUBLE_STAR_END": r".*/.*",
    "DOUBLE_STAR": r"((/.+/)|/)",
    "SPACE": r"\ ",
    "STAR_END": r"[^/]*",
    "STAR": r"[^/]*",
    "SLASH_START": r"",
    "SLASH_END": r"/",
    "SLASH": r"/",
}

anchoring_tokens = {"SLASH", "SLASH_START", "DOUBLE_STAR"}
slash_tokens = {"SLASH", "SLASH_END", "DOUBLE_STAR", "DOUBLE_STAR_START"}


def gitglob_to_regex(glob_pattern: str) -> Tuple[re.Pattern, re.Pattern]:
    tokens = list(glob_lexer.tokenize(glob_pattern))

    # get inner regex
    core_regex = ""
    only_left_anchoring = set([token.type for token in tokens]) & anchoring_tokens or glob_pattern == '*'
    left_anchored_prefix = ""
    for token in tokens:
        log.debug(f"- token: {token.type} ({token.value})")
        if token.type == "TEXT":
            core_regex += fnmatch.translate(token.value)[4:-3]
        elif token.type == "CHARACTER_CLASS":
            core_regex += character_class_to_regex(token.value)
        elif token.type == "DOUBLE_STAR_START":
            left_anchored_prefix = "((.+/)|/)?"
        else:
            core_regex += regex_map.get(token.type, token.value)

    # get final regex
    suffix = "" if token.type in slash_tokens else "(/|$)"
    left_anchored_regex = f"^{left_anchored_prefix}{core_regex}{suffix}"
    if only_left_anchoring:
        regex = left_anchored_regex
    else:
        right_anchored_regex = f".*/{core_regex}{suffix}$"
        regex = f"({left_anchored_regex})|({right_anchored_regex})"

    return re.compile(regex)
