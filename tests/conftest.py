import shutil
from pathlib import Path

import pytest
from sec_edgar_downloader import Downloader


@pytest.fixture(scope="function")
def downloader(tmpdir):
    tmp_dir = Path(tmpdir.mkdir("Downloads"))
    dl = Downloader(tmp_dir)
    yield dl, tmp_dir
    shutil.rmtree(tmp_dir)


@pytest.fixture(scope="session")
def apple_filing_metadata():
    apple_ticker_data = {
        "symbol": "AAPL",
        "full_cik": "0000320193",
        "company_name": "APPLE INC",
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
