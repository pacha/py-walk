from sly import Lexer

class GlobLexer(Lexer):
    tokens = {
        ESC_SQUARE_BRACKET,  # noqa
        ESC_EXCLAMATION_MARK,  # noqa
        ESC_QUESTION_MARK,  # noqa
        ESC_STAR,  # noqa
        DOUBLE_STAR_START,  # noqa
        DOUBLE_STAR_END,  # noqa
        DOUBLE_STAR_MIDDLE,  # noqa
        CHARACTER_CLASS,  # noqa
        EXCLAMATION_MARK,  # noqa
        SLASH_END,  # noqa
        SLASH,  # noqa
        QUESTION_MARK,  # noqa
        STAR,  # noqa
        TEXT,  # noqa
    }

    # Escape Glob special chars
    ESC_EXCLAMATION_MARK = r"^\\!"
    ESC_SQUARE_BRACKET = r"\\\["
    ESC_QUESTION_MARK = r"\\\?"
    ESC_STAR = r"\\\*"

    # Special ending sequences /$ /**$
    DOUBLE_STAR_START = r"^/?\*\*/"

    # Special middle sequences /**/
    DOUBLE_STAR_MIDDLE = r"/\*\*/"

    # EXC_DOUBLE_STAR_START = r"^(?<=!)/?\*\*/"
    DOUBLE_STAR_END = r"/\*\*$"
    CHARACTER_CLASS = r"\[!?\]?[^]]*\]"
    EXCLAMATION_MARK = r"^!"
    SLASH_END = r"/$"
    SLASH = r"/"
    QUESTION_MARK = r"\?"
    STAR = r"\*"
    TEXT = r"[^[?\\*/]+"


glob_lexer = GlobLexer()
