import logging
from pathlib import Path
from subprocess import run

import yaml
import pytest

from py_walk.logs import log
from py_walk import get_parser_from_file


# change logging settings for testing
@pytest.fixture(autouse=True)
def set_log_level(caplog):
    caplog.set_level(logging.DEBUG, logger="py_walk")


@pytest.fixture(scope="session")
def fixtures_path():
    return Path(__file__).parent / "_fixtures"


@pytest.fixture(scope="session")
def repo_path(tmp_path_factory):
    repo_path = tmp_path_factory.mktemp("repo")
    run(["git", "init", "-b", "main"], cwd=repo_path, capture_output=True)
    return repo_path


def yaml_data(tests_filename):
    # get test cases from YAML file
    yaml_path = Path(__file__).parent / "_fixtures" / tests_filename
    test_cases = yaml.safe_load(yaml_path.read_text())

    # for each test case, produce a parser and a set of paths to test
    for test_case in test_cases:
        patterns = test_case["patterns"]
        for path in test_case.get("matches", []):
            yield (patterns, path, True)
        for path in test_case.get("non_matches", []):
            yield (patterns, path, False)


@pytest.fixture(params=yaml_data("lib-tests.yaml"), scope="session")
def lib_tests(request):
    return request.param


@pytest.fixture(params=yaml_data("git-tests.yaml"), scope="session")
def git_tests(request):
    return request.param


@pytest.fixture
def test_runner():
    def inner_function(repo_path, patterns, path):
        log.debug(f"-- Patterns:\n{patterns}")
        log.debug(f"-- Path: {path}")

        # create gitignore file
        gitignore_path = repo_path / ".gitignore"
        gitignore_path.write_text(patterns)

        # create parser
        parser = get_parser_from_file(gitignore_path)

        # check actual result from Git
        command_result = run(
            ["git", "check-ignore", "--", path],
            cwd=gitignore_path.parent,
            capture_output=True,
        )
        git_result = bool(command_result.returncode == 0)

        # check result from py-walk
        lib_result = parser.match(path)
        return git_result, lib_result

    return inner_function
