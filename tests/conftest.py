"""Pytest fixtures for testing suite."""


import shutil

import pytest

from sec_edgar_downloader import Downloader
from sec_edgar_downloader._constants import (
    DATE_FORMAT_TOKENS,
    DEFAULT_AFTER_DATE,
    DEFAULT_BEFORE_DATE,
)


@pytest.fixture(scope="function")
def downloader(tmp_path):
    dl = Downloader(tmp_path)
    yield dl, tmp_path
    shutil.rmtree(tmp_path)


@pytest.fixture(scope="session")
def formatted_earliest_after_date():
    return DEFAULT_AFTER_DATE.strftime(DATE_FORMAT_TOKENS)


@pytest.fixture(scope="session")
def formatted_latest_before_date():
    return DEFAULT_BEFORE_DATE.strftime(DATE_FORMAT_TOKENS)
