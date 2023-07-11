"""Pytest fixtures for testing suite."""
import shutil
from unittest.mock import patch

import pytest

from sec_edgar_downloader import Downloader

COMPANY_NAME = "SEC Edgar Downloader Tests"
EMAIL = "foo@bar.com"


@pytest.fixture(scope="function")
def downloader(tmp_path, apple_cik, apple_ticker):
    with patch(
        "sec_edgar_downloader.Downloader.get_ticker_to_cik_mapping"
    ) as mock_ticker_cik_mapping:
        # Mock ticker to CIK mapping to prevent a call to SEC API
        mock_ticker_cik_mapping.return_value = {apple_ticker: apple_cik}
        dl = Downloader(COMPANY_NAME, EMAIL, tmp_path)
        yield dl, tmp_path
        shutil.rmtree(tmp_path)


@pytest.fixture(scope="session")
def form_10k() -> str:
    return "10-K"


@pytest.fixture(scope="session")
def apple_cik() -> str:
    return "0000320193"


@pytest.fixture(scope="session")
def apple_ticker() -> str:
    return "AAPL"
