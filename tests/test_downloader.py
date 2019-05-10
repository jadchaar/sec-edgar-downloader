import os
import pytest
from sec_edgar_downloader import Downloader
from utils import verify_directory_structure


def test_8k_filings(default_download_folder):
    filing_type = "8-K"
    dl = Downloader(default_download_folder)

    apple_ticker = "AAPL"
    num_downloaded = dl.get_8k_filing(apple_ticker, 1)
    assert num_downloaded == 1

    num_downloaded = dl.get_8k_filing(apple_ticker, 0)
    assert num_downloaded == 0

    # Vanguard Group (CIK: 0000102909) does not file 8-Ks
    num_downloaded = dl.get_8k_filing("0000102909")
    assert num_downloaded == 0
    num_downloaded = dl.get_8k_filing("102909")
    assert num_downloaded == 0

    # Verify directory content
    dir_content = os.listdir(default_download_folder)
    assert len(dir_content) == 1
    assert dir_content[0] == "sec-edgar-filings"

    verify_directory_structure(default_download_folder, "AAPL", "0000320193", "8-K")

# TODO: test throwing IO error in ctor
