import re
import fnmatch

from sly import Lexer

from gitignore_match.logs import log


class GlobLexer(Lexer):
    tokens = {
        ESC_EXCLAMATION_MARK,  # noqa
        ESC_SQUARE_BRACKET,  # noqa
        ESC_QUESTION_MARK,  # noqa
        ESC_STAR,  # noqa
        DOUBLE_STAR_START,  # noqa
        CHARACTER_CLASS,  # noqa
        QUESTION_MARK,  # noqa
        DOUBLE_STAR,  # noqa
        STAR,  # noqa
        SLASH_END,  # noqa
        SLASH,  # noqa
        ATOM,  # noqa
    }

    ESC_EXCLAMATION_MARK = r"\\!"
    ESC_SQUARE_BRACKET = r"\\\["
    ESC_QUESTION_MARK = r"\\\?"
    ESC_STAR = r"\\\*"
    DOUBLE_STAR_START = r"^((\*\*/)|(/\*\*/))"
    CHARACTER_CLASS = r"\[!?\]?[^]]*\]"
    QUESTION_MARK = r"\?"
    DOUBLE_STAR = r"/\*\*/"
    STAR = r"\*"
    SLASH_END = r"/$"
    SLASH = r"/"
    ATOM = r"[^/[\\]+"


glob_lexer = GlobLexer()

regex_map = {
    "ESC_EXCLAMATION_MARK": r"!",
    "ESC_QUESTION_MARK": r"\?",
    "ESC_SQUARE_BRACKET": r"\[",
    "ESC_STAR": r"\*",
    "DOUBLE_STAR_START": r"((.+/)|/)",
    "QUESTION_MARK": r".",
    "DOUBLE_STAR": r"((/.+/)|/)",
    "STAR": r"[^/]*",
    "SLASH_END": r"/",
    "SLASH": r"/",
}

anchoring_tokens = {"SLASH", "DOUBLE_STAR"}
slash_tokens = {"SLASH", "SLASH_END", "DOUBLE_STAR", "DOUBLE_STAR_START"}

def gitglob_to_regex(glob_pattern: str) -> re.Pattern:
    log.debug(f"glob: {glob_pattern}")
    regex = ""
    tokens = list(glob_lexer.tokenize(glob_pattern))
    only_left_anchoring = set([token.type for token in tokens]) & anchoring_tokens
    log.debug(f"anchoring: {only_left_anchoring}")
    left_anchored_prefix = ""
    for token in tokens:
        log.debug(f"- token: {token.type} ({token.value})")
        if token.type in ("ATOM", "CHARACTER_CLASS"):
            regex += fnmatch.translate(token.value)[4:-3]
        elif token.type == "DOUBLE_STAR_START":
            left_anchored_prefix = "((.+/)|/)"
        else:
            regex += regex_map.get(token.type, token.value)
    suffix = "(.*)?" if token.type in slash_tokens else "(/.*)?"
    left_anchored_regex = f"^{left_anchored_prefix}{regex}{suffix}$"
    if only_left_anchoring:
        final_regex = left_anchored_regex
    else:
        log.debug(f"here: {only_left_anchoring}")
        suffix = "/?" if token.type not in slash_tokens else ""
        right_anchored_regex = f"^(.*/)?{regex}{suffix}$"
        final_regex = f"({left_anchored_regex})|({right_anchored_regex})"
    return re.compile(final_regex)