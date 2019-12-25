"""Pytest fixtures for testing suite."""

import shutil

import pytest

from sec_edgar_downloader import Downloader
from sec_edgar_downloader._utils import form_query_string


@pytest.fixture(scope="function")
def downloader(tmp_path):
    tmp_dir = tmp_path.joinpath("Downloads")
    tmp_dir.mkdir()
    dl = Downloader(tmp_dir)
    yield dl, tmp_dir
    shutil.rmtree(tmp_dir)


@pytest.fixture(scope="session")
def apple_10k_edgar_search_xml_url():
    qs = form_query_string("AAPL", "10-K", "20190531")
    return f"https://www.sec.gov/cgi-bin/browse-edgar?{qs}"


@pytest.fixture(scope="session")
def apple_filing_metadata():
    apple_ticker_data = {
        "symbol": "AAPL",
        "full_cik": "0000320193",
        "company_name": "APPLE INC",
    }
    return apple_ticker_data


@pytest.fixture(scope="session")
def apple_filing_metadata_pre_2007():
    """
    Prior to 2007, Apple filed with the SEC as
    APPLE COMPUTER INC rather than APPLE INC
    """
    apple_ticker_data = {
        "symbol": "AAPL",
        "full_cik": "0000320193",
        "company_name": "APPLE COMPUTER INC",
    }
    return apple_ticker_data


@pytest.fixture(scope="session")
def vanguard_filing_metadata():
    vanguard_ticker_data = {
        "symbol": None,
        "full_cik": "0000102909",
        "company_name": "VANGUARD GROUP INC",
    }
    return vanguard_ticker_data
