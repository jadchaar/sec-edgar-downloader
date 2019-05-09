import pytest
import os
from sec_edgar_downloader import Downloader
from pathlib import Path

def test_8k_filings(default_download_folder):
    dl = Downloader(default_download_folder)

    ticker = "AAPL"
    num_downloaded = dl.get_8k_filing(ticker, 1)
    assert num_downloaded == 1

    num_downloaded = dl.get_8k_filing(ticker, 0)
    assert num_downloaded == 0

    # Vanguard Group (CIK: 0000102909) does not file 8Ks
    num_downloaded = dl.get_8k_filing("0000102909")
    assert num_downloaded == 0
    num_downloaded = dl.get_8k_filing("102909")
    assert num_downloaded == 0

    dir_content = os.listdir(default_download_folder)
    assert len(dir_content) == 1
    assert dir_content[0] == "sec-edgar-filings"

    next_level_of_dir = str(Path.joinpath(Path(default_download_folder), "sec-edgar-filings"))
    dir_content = os.listdir(next_level_of_dir)
    assert len(dir_content) == 1
    assert dir_content[0] == ticker

    next_level_of_dir = str(Path.joinpath(Path(next_level_of_dir), ticker))
    dir_content = os.listdir(next_level_of_dir)
    assert len(dir_content) == 1
    assert dir_content[0] == "8-K"

    next_level_of_dir = str(Path.joinpath(Path(next_level_of_dir), "8-K"))
    dir_content = os.listdir(next_level_of_dir)
    assert len(dir_content) == 1
    assert Path(dir_content[0]).suffix == ".txt"
