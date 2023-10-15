import logging
from pathlib import Path

import pytest


# change logging settings for testing
@pytest.fixture(autouse=True)
def set_log_level(caplog):
    caplog.set_level(logging.DEBUG, logger="gitignore_match")


@pytest.fixture(scope="session")
def fixtures_path():
    return Path(__file__).parent / "_fixtures"
