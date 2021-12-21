"""Pytest fixtures for testing suite."""


import shutil
import time

import pytest

from sec_edgar_downloader import Downloader
from sec_edgar_downloader._constants import (
    DATE_FORMAT_TOKENS,
    DEFAULT_AFTER_DATE,
    DEFAULT_BEFORE_DATE,
    SEC_EDGAR_RATE_LIMIT_SLEEP_INTERVAL,
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


@pytest.fixture(autouse=True)
def prevent_rate_limit():
    """Prevent SEC rate-limiting by sleeping between test cases."""
    yield
    time.sleep(SEC_EDGAR_RATE_LIMIT_SLEEP_INTERVAL)
