
from gitignore_match import parse_pattern_file

def test_entrypoint_parse_pattern_file(fixtures_path):

    patterns_path = fixtures_path / "pattern-files" / "basic-question-mark"
    patterns = parse_pattern_file(patterns_path)
    assert patterns.match("abc") is not None
    assert patterns.match("acc") is not None
    assert patterns.match("abcc") is None
