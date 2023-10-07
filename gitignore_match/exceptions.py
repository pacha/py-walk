
class GitignoreMatchException(Exception):
    """GitignoreMatch base exeption."""

    pass


class GitignoreMatchError(GitignoreMatchException):
    """Base exeption for GitignoreMatch errors."""

    pass


class GitignoreMatchInputError(GitignoreMatchError):
    """Invalid user provided data."""

    pass


class GitignoreMatchInternalError(GitignoreMatchError):
    """Exeption for internal, unexpected errors."""

    pass

