import shutil
import sys
import pytest
from pathlib import Path
from sec_edgar_downloader import Downloader

sys.path.append(str(Path(__file__).parent.joinpath('helpers')))


@pytest.fixture(scope="function")
def downloader(tmpdir):
    tmp_dir = Path(tmpdir.mkdir("Downloads"))
    dl = Downloader(tmp_dir)
    yield dl, tmp_dir
    shutil.rmtree(tmp_dir)


@pytest.fixture(scope="session")
def apple_filing_metadata():
    apple_ticker_data = {
        "ticker_symbol": "AAPL",
        "ticker_full_cik": "0000320193"
    }
    return apple_ticker_data


@pytest.fixture(scope="session")
def vanguard_filing_metadata():
    vanguard_ticker_data = {
        "ticker_symbol": None,
        "ticker_full_cik": "0000102909"
    }
    return vanguard_ticker_data
