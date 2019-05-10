import os
from pathlib import Path

import pytest

from sec_edgar_downloader import Downloader
from utils import parse_filing_document_header


def test_8k_filings(default_download_folder):
    filing_type = "8-K"
    dl = Downloader(default_download_folder)

    apple_ticker = "AAPL"
    num_downloaded = dl.get_8k_filing(apple_ticker, 1)
    assert num_downloaded == 1

    num_downloaded = dl.get_8k_filing(apple_ticker, 0)
    assert num_downloaded == 0

    # Vanguard Group (CIK: 0000102909) does not file 8Ks
    num_downloaded = dl.get_8k_filing("0000102909")
    assert num_downloaded == 0
    num_downloaded = dl.get_8k_filing("102909")
    assert num_downloaded == 0

    # Verify directory content
    dir_content = os.listdir(default_download_folder)
    assert len(dir_content) == 1
    assert dir_content[0] == "sec-edgar-filings"

    next_level_of_dir = Path.joinpath(default_download_folder, "sec-edgar-filings")
    assert next_level_of_dir.is_dir()
    dir_content = os.listdir(next_level_of_dir)
    assert len(dir_content) == 1
    assert dir_content[0] == apple_ticker

    next_level_of_dir = Path.joinpath(next_level_of_dir, apple_ticker)
    assert next_level_of_dir.is_dir()
    dir_content = os.listdir(next_level_of_dir)
    assert len(dir_content) == 1
    assert dir_content[0] == filing_type

    next_level_of_dir = Path.joinpath(next_level_of_dir, filing_type)
    assert next_level_of_dir.is_dir()
    dir_content = os.listdir(next_level_of_dir)
    assert len(dir_content) == 1

    next_level_of_dir = Path.joinpath(next_level_of_dir, dir_content[0])
    assert next_level_of_dir.is_file()
    assert next_level_of_dir.suffix == ".txt"

    accession_number = next_level_of_dir.stem
    apple_cik = "0000320193"
    assert accession_number[:len(apple_cik)] == apple_cik

    header_contents = parse_filing_document_header(next_level_of_dir)
    assert header_contents["ACCESSION NUMBER"] == accession_number
    assert header_contents["CONFORMED SUBMISSION TYPE"] == filing_type

# TODO: test throwing IO error in ctor
