# mypy: disable-error-code="name-defined"
import re

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
        CHARACTER_CLASS,  # noqa
        QUESTION_MARK,  # noqa
        STAR,  # noqa
        TEXT,  # noqa
    }

    ESC_EXCLAMATION_MARK = r"\\!"
    ESC_SQUARE_BRACKET = r"\\\["
    ESC_QUESTION_MARK = r"\\\?"
    ESC_SPACE = r"\\ "
    ESC_STAR = r"\\\*"
    CHARACTER_CLASS = r"\[(\^|!)?\]?-?(\[:[a-z]+:\]|(\\\]|\\-|[^]-])-(\\\]|\\-|[^]-])|\\\]|\\-|[^]-])*-?\]"
    QUESTION_MARK = r"\?"
    STAR = r"\*"
    TEXT = r"[^[*?\\]+"


glob_lexer = GlobLexer()

regex_map = {
    "ESC_EXCLAMATION_MARK": r"!",
    "ESC_SQUARE_BRACKET": r"\[",
    "ESC_QUESTION_MARK": r"\?",
    "ESC_SPACE": r"\ ",
    "ESC_STAR": r"\*",
    "QUESTION_MARK": r".",
    "STAR": r"[^/]*",
}


def glob_to_regex(glob_pattern: str) -> re.Pattern:
    tokens = glob_lexer.tokenize(glob_pattern)
    regex = ""
    for token in tokens:
        log.debug(f"- token: {token.type} ({token.value})")
        if token.type == "TEXT":
            regex += token.value
        elif token.type == "CHARACTER_CLASS":
            regex += character_class_to_regex(token.value)
        else:
            regex += regex_map.get(token.type, token.value)
    return re.compile(regex)
