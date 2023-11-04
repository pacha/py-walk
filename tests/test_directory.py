from subprocess import run

import pytest

from py_walk import get_parser_from_file


@pytest.fixture(scope="session")
def repo_path(tmp_path_factory):
    # create repository
    path = tmp_path_factory.mktemp("repo")
    run(["git", "init", "-b", "main"], cwd=path, capture_output=True)

    # create gitignore file
    gitignore_path = path / ".gitignore"
    gitignore_path.write_text("my_dir/")
    return path


@pytest.fixture(scope="session")
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
