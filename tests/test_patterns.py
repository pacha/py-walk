from pathlib import Path
from subprocess import run

import yaml
import pytest

from gitignore_match.logs import log
from gitignore_match import get_parser_from_file


@pytest.fixture(scope="session")
def repo_path(tmp_path_factory):
    repo_path = tmp_path_factory.mktemp("repo")
    run(["git", "init", "-b", "main"], cwd=repo_path, capture_output=True)
    return repo_path


def yaml_data():
    # get test cases from YAML file
    yaml_path = Path(__file__).parent / "_fixtures" / "test-cases.yaml"
    test_cases = yaml.safe_load(yaml_path.read_text())

    # for each test case, produce a parser and a set of paths to test
    for test_case in test_cases:
        patterns = test_case["patterns"]
        for path in test_case.get("matches", []):
            yield (patterns, path, True)
        for path in test_case.get("non_matches", []):
            yield (patterns, path, False)

@pytest.fixture(params=yaml_data(), scope="session")
def path_test(request):
    return request.param


def test_gitignore_patterns(repo_path, path_test):
    """Test a single path against a gitignore-like file."""

    # get patterns and path
    patterns, path, expected = path_test
    log.debug(f"-- Patterns:\n{patterns}")
    log.debug(f"-- Path: {path}")

    # create gitignore file
    gitignore_path = repo_path / ".gitignore"
    gitignore_path.write_text(patterns)

    # create parser
    parser = get_parser_from_file(gitignore_path)

    # check actual result from Git
    command_result = run(["git", "check-ignore", path], cwd=gitignore_path.parent, capture_output=True)
    git_result = bool(command_result.returncode == 0)

    # check result from gitignore-match
    lib_result = parser.match(path)

    log.debug(f"Git result: {git_result}")
    log.debug(f"Lib result: {lib_result}")
    log.debug(f"Expected: {expected}")
    assert (git_result == lib_result)
    assert (lib_result == expected)
