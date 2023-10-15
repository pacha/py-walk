from pathlib import Path
from subprocess import run

import pytest


@pytest.fixture(scope="session")
def fixtures_path():
    return Path(__file__).parent / "_fixtures"

@pytest.fixture(scope="session")
def repo_path(tmp_path_factory):
    repo_dir = tmp_path_factory.mktemp("repo")
    run(["git", "init", "-b", "main"], cwd=repo_dir, capture_output=True)
    return repo_dir
