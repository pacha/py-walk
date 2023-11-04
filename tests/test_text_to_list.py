from textwrap import dedent
from py_walk import pattern_text_to_pattern_list


def test_pattern_text_to_pattern_list():
    text = dedent(
        """
        # text files
        *.txt
          *.md

        # python files
        __pycache__/
        *.py[cod]
    """
    )
    expected_patterns = ["*.txt", "*.md", "__pycache__/", "*.py[cod]"]
    patterns = pattern_text_to_pattern_list(text)
    assert patterns == expected_patterns
