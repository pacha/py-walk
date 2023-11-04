from py_walk.logs import log


def test_lib_cases(repo_path, lib_tests, test_runner):
    """Run test cases created during the development of the library."""

    # get patterns and path
    patterns, path, expected = lib_tests
    git_result, lib_result = test_runner(repo_path, patterns, path)
    log.debug(f"Git result: {git_result}")
    log.debug(f"Lib result: {lib_result}")
    log.debug(f"Expected: {expected}")
    assert git_result == lib_result
    assert lib_result == expected
