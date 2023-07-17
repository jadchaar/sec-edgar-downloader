"""Pytest fixtures for testing suite."""
import shutil
from typing import Any
from unittest.mock import patch

import pytest

from sec_edgar_downloader import Downloader


@pytest.fixture(scope="function")
def downloader(tmp_path, apple_cik, apple_ticker, company_name, email):
    with patch(
        "sec_edgar_downloader.Downloader.get_ticker_to_cik_mapping"
    ) as mock_ticker_cik_mapping:
        # Mock ticker to CIK mapping to prevent a call to SEC API
        mock_ticker_cik_mapping.return_value = {apple_ticker: apple_cik}
        dl = Downloader(company_name, email, tmp_path)
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


@pytest.fixture(scope="session")
def company_name() -> str:
    return "SEC Edgar Downloader Tests"


@pytest.fixture(scope="session")
def email() -> str:
    return "foo@bar.com"


@pytest.fixture(scope="session")
def user_agent(company_name, email) -> str:
    return f"{company_name} {email}"


@pytest.fixture(scope="session")
def accession_number() -> str:
    return "0000320193-22-000108"


@pytest.fixture(scope="session")
def form_4_primary_doc() -> str:
    return "xslF345X04/wf-form4_168444912415136.xml"


@pytest.fixture(scope="session")
def form_8k_primary_doc() -> str:
    return "ny20007635x4_8k.htm"


@pytest.fixture(scope="session")
def sample_cik_ticker_payload() -> Any:
    return {
        "fields": ["cik", "name", "ticker", "exchange"],
        "data": [
            [320193, "Apple Inc.", "AAPL", "Nasdaq"],
            [789019, "MICROSOFT CORP", "MSFT", "Nasdaq"],
            [1652044, "Alphabet Inc.", "GOOGL", "Nasdaq"],
            [1018724, "AMAZON COM INC", "AMZN", "Nasdaq"],
        ],
    }
