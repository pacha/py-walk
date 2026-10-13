import os
import sys
from subprocess import run

import pytest

# the probe holds no non-ASCII character, because it runs under a locale that
# cannot decode one
PROBE = """\
from py_walk import get_parser_from_file

parser = get_parser_from_file(".gitignore")
print(parser.match("caf\\u00e9/menu.txt"))
"""


@pytest.fixture(scope="function")
def repo_path(tmp_path_factory):
    # create repository
    path = tmp_path_factory.mktemp("repo")
    run(["git", "init", "-b", "main"], cwd=path, capture_output=True)

    # create gitignore file with a non-ASCII pattern, encoded as UTF-8
    gitignore_path = path / ".gitignore"
    gitignore_path.write_bytes("café/\n".encode("utf-8"))
    return path


def test_non_ascii_pattern_under_non_utf8_locale(repo_path):
    """Non-ASCII pattern, file read under a locale that is not UTF-8."""
    path = "café/menu.txt"
    command = run(
        ["git", "check-ignore", "--", path], cwd=repo_path, capture_output=True
    )
    git_result = bool(command.returncode == 0)

    # match the same path from an interpreter whose locale encoding is ASCII
    env = dict(os.environ, LC_ALL="C", PYTHONCOERCECLOCALE="0", PYTHONUTF8="0")
    probe = run(
        [sys.executable, "-c", PROBE], cwd=repo_path, env=env, capture_output=True
    )
    assert probe.returncode == 0, probe.stderr.decode(errors="replace")
    lib_result = probe.stdout.decode().strip() == "True"
    assert git_result == lib_result
