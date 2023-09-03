"""Pytest fixtures for testing suite."""
import json
import shutil
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Union
from unittest.mock import patch

import pytest

from sec_edgar_downloader import Downloader


@pytest.fixture(scope="function")
def downloader(tmp_path, apple_cik, apple_ticker, company_name, email):
    with patch(
        "sec_edgar_downloader.Downloader.get_ticker_to_cik_mapping", autospec=True
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


@pytest.fixture(scope="session")
def sample_ticker_to_cik_mapping() -> Any:
    return {"AAPL": "0000320193", "MSFT": "0000789019"}


@pytest.fixture(scope="session")
def accession_number_to_metadata() -> Dict[str, Dict[str, Union[str, date]]]:
    test_data_path = Path(__file__).parent / "test_data"
    filing_data = []
    for p in test_data_path.glob("*.json"):
        with p.open() as f:
            json_output = json.load(f)
        # First page of SEC Edgar API response
        if "filings" in json_output:
            filing_data.append(json_output["filings"]["recent"])
        # Second page onward of SEC Edgar API response
        else:
            filing_data.append(json_output)

    accession_number_to_metadata = {}
    for fd in filing_data:
        acc_nums = fd["accessionNumber"]
        for idx, acc_num in enumerate(acc_nums):
            acc_num_metadata = {}
            for key in fd.keys():
                if key == "accessionNumber":
                    continue
                if key == "filingDate":
                    acc_num_metadata[key] = datetime.strptime(
                        fd[key][idx], "%Y-%m-%d"
                    ).date()
                else:
                    acc_num_metadata[key] = fd[key][idx]
            accession_number_to_metadata[acc_num] = acc_num_metadata

    assert len(accession_number_to_metadata) == 1988

    return accession_number_to_metadata
