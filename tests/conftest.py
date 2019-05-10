import shutil
import sys
import pytest
from pathlib import Path

sys.path.append(str(Path(__file__).parent.joinpath('helpers')))


@pytest.fixture(scope="function")
def default_download_folder(tmpdir):
    tmp = Path(tmpdir.mkdir("Downloads"))
    yield tmp
    shutil.rmtree(tmp)


@pytest.fixture(scope="session")
def apple_filing_metadata():
    apple_ticker_data = {
        "ticker_symbol": "AAPL",
        "ticker_cik": "0000320193"
    }
    return apple_ticker_data
