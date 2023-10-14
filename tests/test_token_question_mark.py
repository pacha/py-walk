import pytest

from dataclasses import dataclass
from gitignore_match.logs import log
from gitignore_match.models import Pattern

@dataclass
class Check:
    glob: str
    path: str
    result: bool


check_list = [
    Check(glob="?", path="a", result=True),
    Check(glob="?", path="aa", result=False),
    Check(glob="?", path="a/a", result=True),
    Check(glob="?", path="c", result=True),
    Check(glob="?", path="aa", result=False),
    Check(glob="a?c", path="abc", result=True),
    Check(glob="a?c", path="abbc", result=False),
    Check(glob="a?c", path="ac", result=False),
    Check(glob="a?c", path="a", result=False),
    Check(glob="a??c", path="abbc", result=True),
    Check(glob=r"a\?c", path="abc", result=False),
    Check(glob=r"a\?c", path=r"a?c", result=True),
    Check(glob=r"a\?\?c", path=r"a??c", result=True),
    Check(glob=r"a*c", path=r"abc", result=True),
    Check(glob=r"a*c", path=r"ababc", result=True),
    Check(glob=r"a*c", path=r"ac", result=True),
    Check(glob=r"a\*c", path=r"a*c", result=True),
    Check(glob=r"a\*c", path=r"abc", result=False),
    Check(glob=r"a\*c", path=r"ababc", result=False),
    Check(glob=r"a\*c", path=r"ababc", result=False),
    Check(glob=r"**/foo.txt", path=r"foo.txt", result=True),
    Check(glob=r"**/foo.txt", path=r"a/b/foo.txt", result=True),
    Check(glob=r"**/c/foo.txt", path=r"a/b/c/foo.txt", result=True),
    Check(glob=r"**/?/foo.txt", path=r"a/bc/foo.txt", result=False),
    Check(glob=r"**/??/foo.txt", path=r"a/bc/foo.txt", result=True),
    Check(glob=r"/**/foo.txt", path=r"foo.txt", result=True),
    Check(glob=r"/**/foo.txt", path=r"a/b/foo.txt", result=True),
    Check(glob=r"/**/c/foo.txt", path=r"a/b/c/foo.txt", result=True),
    Check(glob=r"/**/?/foo.txt", path=r"a/bc/foo.txt", result=False),
    Check(glob=r"/**/??/foo.txt", path=r"a/bc/foo.txt", result=True),
    Check(glob=r"a**/foo.txt", path=r"abfoo.txt", result=False),
    Check(glob=r"**/", path=r"foo.txt", result=False),
    Check(glob=r"**/", path=r"a/foo.txt", result=True),
    Check(glob=r"[a]", path=r"a", result=True),
    Check(glob=r"a[bc]d", path=r"abd", result=True),
    Check(glob=r"a[bc]d", path=r"azd", result=False),
    Check(glob=r"a[bcd]d", path=r"add", result=True),
    Check(glob=r"a[!bc]d", path=r"abd", result=False),
    Check(glob=r"A[z-a]D", path=r"AmD", result=False),
    Check(glob=r"[!a-z]", path=r"a", result=False),
    Check(glob=r"[!a-z]", path=r"A", result=True),
    Check(glob=r"[]a-z]", path=r"m", result=True),
    Check(glob=r"[]a-z]", path=r"]", result=True),
    Check(glob=r"[]a-z]", path=r"[", result=False),
    Check(glob=r"[!]a-z]", path=r"]", result=False),
    Check(glob=r"[!]a-z]", path=r"s", result=False),
    Check(glob=r"[!]a-z]", path=r"S", result=True),
    Check(glob=r"[]-]", path=r"]", result=True),
    Check(glob=r"[]-]", path=r"-", result=True),
    Check(glob=r"[]-]", path=r"a", result=False),
    Check(glob=r"a]b", path=r"a]b", result=True),
    Check(glob=r"a\[b", path=r"a[b", result=True),
    Check(glob=r"a[b", path=r"a[b", result=False),
    Check(glob=r"!abc", path=r"abc", result=False),
    Check(glob=r"!abc", path=r"abd", result=True),
    Check(glob=r"\!abc", path=r"!abc", result=True),
    Check(glob=r"a/**/z", path=r"a/b/z", result=True),
    Check(glob=r"a/**/z", path=r"a/b/c/z", result=True),
    Check(glob=r"a/**/z", path=r"a/b/c/x/z", result=True),
]

@pytest.fixture(params=check_list)
def check(request):
    return request.param

def test_token_question_mark(check):
    log.debug(f"\npath: {check.path}")
    pattern = Pattern(check.glob)
    log.debug(f"result: {check.result}")
    assert pattern.match(check.path) == check.result
