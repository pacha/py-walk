from py_walk.logs import log


def test_git_cases(repo_path, git_tests, test_runner):
    """Run test cases originally created in the git project."""

    # get patterns and path
    patterns, path, expected = git_tests
    git_result, lib_result = test_runner(repo_path, patterns, path)
    log.debug(f"Git result: {git_result}")
    log.debug(f"Lib result: {lib_result}")
    log.debug(f"Expected: {expected}")
    assert git_result == lib_result
    assert lib_result == expected
