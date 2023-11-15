from subprocess import run

import pytest

from py_walk import get_parser_from_file
from py_walk import get_parser_from_list


@pytest.fixture(scope="function")
def repo_path(tmp_path_factory):
    # create repository
    path = tmp_path_factory.mktemp("repo")
    run(["git", "init", "-b", "main"], cwd=path, capture_output=True)

    # create gitignore file
    gitignore_path = path / ".gitignore"
    gitignore_path.write_text("my_dir/")
    return path


@pytest.fixture(scope="function")
def parser(repo_path):
    gitignore_path = repo_path / ".gitignore"
    return get_parser_from_file(gitignore_path)


def test_slash_in_pattern_but_not_in_path(repo_path, parser):
    """Slash in pattern but not in path (no directory created)."""
    path = "my_dir"
    command = run(
        ["git", "check-ignore", "--", path], cwd=repo_path, capture_output=True
    )
    git_result = bool(command.returncode == 0)
    lib_result = parser.match(path)
    assert git_result == lib_result


def test_slash_in_pattern_and_in_path(repo_path, parser):
    """Slash in pattern and path (no directory created)."""
    path = "my_dir/"
    command = run(
        ["git", "check-ignore", "--", path], cwd=repo_path, capture_output=True
    )
    git_result = bool(command.returncode == 0)
    lib_result = parser.match(path)
    assert git_result == lib_result


def test_slash_in_pattern_but_not_in_path_dir_exists(repo_path, parser):
    """Slash in pattern but not in path (directory created)."""
    path = "my_dir"
    (repo_path / path).mkdir()
    command = run(
        ["git", "check-ignore", "--", path], cwd=repo_path, capture_output=True
    )
    git_result = bool(command.returncode == 0)
    lib_result = parser.match(path)
    assert git_result == lib_result


def test_no_base_dir(repo_path, parser):
    """When no base_dir is provided the library can't check if the provided path is a directory."""
    path = "my_dir"
    (repo_path / path).mkdir()
    command = run(
        ["git", "check-ignore", "--", path], cwd=repo_path, capture_output=True
    )
    git_result = bool(command.returncode == 0)

    # git will check that the path is actually a directory and return that there's a match
    assert git_result is True

    # with no base dir, the library won't be able to resolve the match correctly
    parser_dir = get_parser_from_list(["my_dir/"])
    assert parser_dir.match(path) is False

    # however, with no trailing slash, the pattern will match directories and files
    parser_file = get_parser_from_list(["my_dir"])
    assert parser_file.match(path) is True
